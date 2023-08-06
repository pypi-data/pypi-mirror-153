"""sonusai tplot

usage: tplot [-hv] [-r ROOT] [-c CONFIG] [-t TARGET] [-m MODEL] [-f FEATURE] [--sedthr SEDTHR]

options:
   -h, --help
   -v, --verbose            Be verbose.
   -r, --root ROOT          Root of a gentcst tree.
   -c, --config CONFIG      YAML config file.
   -t, --target TARGET      Target .wav or .txt, else use target section in CONFIG.
   -m, --model MODEL        Aaware ONNX model file.
   -f, --feature FEATURE    Feature override, e.g., gfh64to128.
   --sedthr SEDTHR          SED thresholds override, e.g., '[-24, -27, -30]'.

   CONFIG is used to override the default configuration, thus it does not need to be a complete
   genmixdb config parameter set, only desired overrides like truth function and truth config.

   A TARGET .txt file supports the same format as SonusAI genmixdb which is a list of regexes
   for finding sound files.

   ROOT, CONFIG, and TARGET are optional, but at least one of them must be specified.
   Behavior is as follows in order of precedence:

    1)  If ROOT is provided, use the given directory as the root directory of
        a gentcst tree. The config will be generated from the top down to the current leaf.
    2)  If CONFIG is provided, use the given YAML file to override the config.
    3)  If TARGET is provided, use the given .wav or .txt file to override the target
        section of the config.
    4)  If FEATURE and/or SEDTHR are provided, use them to override the config.

   If TARGET is given without a CONFIG, look for a corresponding YAML file to use as a
   config. For example,

        sonusai tplot -t 4-esc50-dogbark.txt

   will first look for '4-esc50-dogbark.yml' and then for 'config.yml'. If neither
   candidate was found and ROOT was also not specified then give an error. If
   ROOT was specified then use the hierarchical config.

   A multi-page plot TARGET-tplot.pdf or CONFIG-tplot.pdf is generated.

"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
import yaml
from docopt import docopt
from matplotlib.backends.backend_pdf import PdfPages
from pyaaware import Predict

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.genft import genft
from sonusai.genmix import genmix
from sonusai.genmixdb import genmixdb
from sonusai.mixture import load_config
from sonusai.mixture import get_default_config
from sonusai.mixture import update_config_from_file
from sonusai.mixture import update_config_from_hierarchy
from sonusai.utils import int16_to_float
from sonusai.utils import trim_docstring


def tplot(root: str = None,
          config_file: str = None,
          target_file: str = None,
          model_file: str = None,
          feature: str = None,
          thresholds: str = None,
          verbose: bool = False) -> None:
    figsize = (11, 8.5)

    if config_file is None and target_file is None and root is None:
        raise SonusAIError('Error: No config provided.')

    target_path = ''
    config = get_default_config()

    if root is not None:
        leaf = os.getcwd()
        target_path = os.path.basename(leaf)
        config = update_config_from_hierarchy(root=root, leaf=leaf, config=config)
        logger.debug(f'Hierarchical config for {leaf} using {root} as the root')

    if config_file is not None:
        target_path = config_file
        config = update_config_from_file(config_file, config)
        logger.debug(f'Config from {config_file}')

    if target_file is not None:
        target_path = target_file
        if not os.path.exists(target_file):
            raise SonusAIError(f'{target_file} does not exist.')

        config['targets'] = [{'target_name': target_file}]
        logger.debug(f'Targets from {target_file}')

        if config_file is None:
            target_config = f'{os.path.splitext(target_file)[0]}.yml'
            if os.path.exists(target_config):
                config = update_config_from_file(target_config, config)
                logger.debug(f'Config from {target_config}')
            else:
                target_config = 'config.yml'
                if os.path.exists(target_config):
                    config = update_config_from_file(target_config, config)
                    logger.debug(f'Config from {target_config}')
                elif root is None:
                    raise SonusAIError(f'Error: Could not determine config for {target_file}.')

    file_base = os.path.splitext(target_path)[0]
    file_name = os.path.split(file_base)[1]
    output = f'./{file_name}-tplot.pdf'

    if len(config['truth_settings']) > 1:
        raise SonusAIError(f'Number of truth_settings is more than one. This is not supported yet.')

    if thresholds is not None:
        thresholds = json.loads(thresholds)
        if thresholds != config['truth_settings'][0]['config']['thresholds']:
            config['truth_settings'][0]['config']['thresholds'] = thresholds
            logger.debug(f'Override SED thresholds with {thresholds}')

    if feature is not None:
        if feature != config['feature']:
            config['feature'] = feature
            logger.debug(f'Override feature with {feature}')

    logger.debug('')

    # Run genmixdb, genmix, and genft
    mixdb = genmixdb(config=config, logging=verbose)
    num_mixtures = len(mixdb['mixtures'])  # Number of mixtures
    logger.info(f'Generating data for {num_mixtures} mixture plots')
    mixture, _, target, noise, _, mixdb_out = genmix(mixdb=mixdb,
                                                     mixid=':',
                                                     compute_segsnr=False,
                                                     compute_truth=False,
                                                     logging=verbose)

    feature_data, truth_f, _, _ = genft(mixdb=mixdb,
                                        mixid=':',
                                        compute_segsnr=False,
                                        logging=verbose)

    # If model provided, read and check it
    predict_data = np.zeros(0)
    if model_file is not None:
        import onnx

        # model is an in-memory ModelProto
        model = onnx.load(model_file)
        if len(model.metadata_props) < 5:
            logger.warn('Model metadata indicates this is not an Aaware model, ignoring.')
        else:
            if model.metadata_props[4].key != 'feature':
                logger.warn('Model metadata does not have Aaware feature, ignoring.')
            else:
                model_feature = model.metadata_props[4].value
                logger.debug(f'Model feature is {model_feature}')
                # TODO Check and read other params, flatten, addch, etc.
                logger.info(f'Running prediction with {model_file}')
                predict = Predict(model_file)
                predict_data = predict.execute(feature_data)

    num_samples = mixture.shape[0]  # Total number of samples over all mixtures
    num_features = feature_data.shape[0]  # Total number of feature frames over all mixtures

    logger.info(f'Plotting {num_mixtures} target-truth results to {output}')
    pdf = PdfPages(f'{output}')
    for m in range(num_mixtures):
        mixture_begin = mixdb_out['mixtures'][m]['i_sample_offset']
        feature_begin = mixdb_out['mixtures'][m]['o_frame_offset']
        # For each target/mixture, get index endpoint (mix,noise,target sample,...)
        if m == num_mixtures - 1:
            mixture_end = num_samples
            feature_end = num_features
        else:
            mixture_end = mixdb_out['mixtures'][m + 1]['i_sample_offset']
            # out frames are possibly decimated/stride-combined
            feature_end = mixdb_out['mixtures'][m + 1]['o_frame_offset']

        # Trim waveform data
        mixture_trimmed = int16_to_float(mixture[mixture_begin:mixture_end])
        target_trimmed = int16_to_float(target[mixture_begin:mixture_end])

        # Provide subset defined by mixture using truth_index array of indices (multichannel truth)
        target_record = mixdb_out['targets'][mixdb_out['mixtures'][m]['target_file_index']]
        truth_settings = target_record['truth_settings']
        if len(truth_settings) > 1:
            raise SonusAIError(f'Number of truth_settings is more than one. This is not supported yet.')

        truth_index = np.array(truth_settings[0]['index']) - 1
        truth_f_trimmed = truth_f[feature_begin:feature_end, truth_index]

        if predict_data.shape[0] > 0:
            predict_data_trimmed = predict_data[feature_begin:feature_end, :]
            # Prediction Activity analysis to select top prediction class
            # true if active in any frame
            predict_activity = np.any(predict_data_trimmed >= mixdb_out['class_weights_threshold'], axis=0)
            predict_activity_index = np.array([i for i, x in enumerate(predict_activity) if x]) + 1
            logger.info(f'Prediction active in classes based on threshold {mixdb_out["class_weights_threshold"]}:\n'
                        f'{predict_activity_index}')
            predict_mean = np.mean(predict_data_trimmed, axis=0)
            top_active_classes = np.argsort(predict_mean)[::-1] + 1
            logger.info(f'Top 10 active prediction classes by mean:\n{top_active_classes[0:10]}')
            # plot most active prediction
            predict_data_trimmed = predict_data_trimmed[:, top_active_classes[0] - 1]
            logger.info(f'Plotting prediction class {top_active_classes[0]}')

        # Setup plot of target waveform with truth on top
        # TODO
        #  Make a function w/args mixture_trimmed, target_trimmed, truth_f, pr, mixdat, m, truth_index, target_path
        # calculate number of samples per frame for plotting
        num_plot_features = truth_f_trimmed.shape[0]
        num_plot_samples_per_feature = len(target_trimmed) // num_plot_features
        # number of plot samples multiple of frames
        num_plot_samples = num_plot_samples_per_feature * num_plot_features
        # x-axis in sec
        x_seconds = np.arange(num_plot_samples, dtype=np.float32) / sonusai.mixture.SAMPLE_RATE
        # Reshape/extend truth to #samples in waveform
        num_plot_classes = truth_f_trimmed.shape[1]  # Number of plot truth classes
        y_truth_f = np.reshape(np.tile(np.expand_dims(truth_f_trimmed, 1), [1, num_plot_samples_per_feature, 1]),
                               [num_plot_samples, num_plot_classes])

        fig, ax0 = plt.subplots(1, 1, constrained_layout=True, figsize=figsize)
        ax = np.array([ax0], dtype=object)
        plots = list()

        # Plot the time-domain waveforms then truth/prediction on second axis
        if mixture_trimmed.shape[0] > 0:
            color = 'mistyrose'
            mix_plot, = ax[0].plot(x_seconds, mixture_trimmed[0:num_plot_samples], color=color, label='MIX')
            ax[0].tick_params(axis='y', labelcolor='red')
            plots.append(mix_plot)

        if target_trimmed.shape[0] > 0:
            color = 'tab:blue'
            tt_plot, = ax[0].plot(x_seconds, target_trimmed[0:num_plot_samples], color=color, label='TAR')
            ax[0].set_ylabel('ampl', color=color)
            ax[0].tick_params(axis='y', labelcolor=color)
            plots.append(tt_plot)

        ax2 = ax[0].twinx()  # instantiate 2nd y-axis that shares the same x-axis

        # Plot first truth
        # TODO Support multi-channel
        if truth_f_trimmed.shape[0] > 0:
            color = 'tab:green'
            label2 = f'truth{truth_index[0] + 1}'
            # we already handled the x-label with ax1
            ax2.set_ylabel(label2, color=color)
            # logger.info(f'Mixture num {m}, truth_index={truth_index}')
            tr_plot, = ax2.plot(x_seconds, y_truth_f[:, 0], color=color, label=label2)
            ax2.set_ylim([-0.05, 1.05])
            ax2.tick_params(axis='y', labelcolor=color)
            plots.append(tr_plot)

        if predict_data.shape[0] > 0:
            color = 'tab:brown'
            label2 = f'prcl{top_active_classes[0]}'
            # we already handled the x-label with ax1
            ax2.set_ylabel(label2, color=color)
            predict_extended = np.reshape(
                np.tile(np.expand_dims(predict_data_trimmed, 1), [1, num_plot_samples_per_feature, 1]),
                [num_plot_samples, num_plot_classes])
            pr_plot, = ax2.plot(x_seconds, predict_extended, color=color, label=label2)
            ax2.set_ylim([-0.05, 1.05])
            ax2.tick_params(axis='y', labelcolor=color)
            plots.append(pr_plot)

        ax[0].set_xlabel('time (s)')  # set only on last/bottom plot

        # Get actual mixture target config parameters
        target_augmentations = mixdb_out['target_augmentations'][mixdb_out['mixtures'][m]['target_augmentation_index']]
        fig.suptitle(
            f'{m + 1} of {num_mixtures}: {target_path}\n'
            f'{target_record["name"]}\n'
            f'Target augmentations: {target_augmentations}\n'
            f'Truth indices: {truth_settings[0]["index"]}\n'
            f'Global Truth Function:Config {truth_settings[0]["function"]} : {truth_settings[0]["config"]}',
            fontsize=10)
        pdf.savefig(fig)
        plt.close(fig)

    # open config file read in as text, then print to last page
    last_page = plt.figure(figsize=figsize)
    last_page.clf()

    option_text = \
        f'Function parameters:\n' \
        f'  root     {root}\n' \
        f'  config   {config_file}\n' \
        f'  target   {target_file}\n' \
        f'  model    {model_file}\n' \
        f'  feature  {feature}\n' \
        f'  sedthr   {thresholds}\n\n' \
        f'----------------------------------------\n\n'
    last_page.text(0.05, 0.95, option_text + yaml.dump(config),
                   transform=last_page.transFigure,
                   family='monospace',
                   size=10,
                   ha="left",
                   va="top")
    pdf.savefig()
    plt.close()
    pdf.close()


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        log_name = 'tplot.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('tplot')

        tplot(root=args['--root'],
              config_file=args['--config'],
              target_file=args['--target'],
              model_file=args['--model'],
              feature=args['--feature'],
              thresholds=args['--sedthr'],
              verbose=verbose)

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
