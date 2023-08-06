"""sonusai predict

usage: predict [-hv] (-m MODEL) (-i INPUT) [-e EXPECT] [-o OUTPUT]

options:
   -h, --help
   -v, --verbose                Be verbose.
   -m MODEL, --model MODEL      Trained model ONNX file.
   -i INPUT, --input INPUT      Input feature WAV or HDF5 file.
   -e EXPECT, --expect EXPECT   Optional expected results HDF5 file.
   -o OUTPUT, --output OUTPUT   Output HDF5 file.

Run prediction on a trained model using SonusAI genft data and optionally
compare the results to expected results.

Inputs:
    MODEL   A SonusAI trained ONNX model file.
    INPUT   A WAV file; or an HDF5 file containing:
                dataset:    feature
    EXPECT  An HDF5 file containing:
                dataset:    predict

Outputs:
    OUTPUT  An HDF5 file containing:
                dataset:    predict
    predict.log

"""
import time
from os.path import exists
from os.path import splitext

import h5py
import numpy as np
from docopt import docopt
from pyaaware import FeatureGenerator
from pyaaware import ForwardTransform
from pyaaware import Predict

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import mixture
from sonusai import update_console_handler
from sonusai.mixture import read_audio
from sonusai.utils import int16_to_float
from sonusai.utils import seconds_to_hms
from sonusai.utils import trim_docstring


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        model_name = args['--model']
        input_name = args['--input']
        expect_name = args['--expect']
        output_name = args['--output']

        start_time = time.monotonic()

        log_name = 'predict.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('predict')

        logger.info('')
        logger.info(f'Model:  {model_name}')
        logger.info(f'Input:  {input_name}')
        logger.info(f'Expect: {expect_name}')
        logger.info(f'Output: {output_name}')
        logger.info('')

        if not output_name and not expect_name:
            raise SonusAIError('Must specify EXPECT or OUTPUT (or both).')

        model = Predict(model_name)
        logger.debug(f'Model input shape {model.input_shape}')
        logger.debug(f'Model output shape {model.output_shape}')

        if not exists(input_name):
            raise SonusAIError(f'{input_name} does not exist')

        ext = splitext(input_name)[1]

        if ext == '.wav':
            audio = read_audio(input_name)

            fft = ForwardTransform(N=mixture.DEFAULT_FRAME_SIZE * 4, R=mixture.DEFAULT_FRAME_SIZE)
            fg = FeatureGenerator(frame_size=mixture.DEFAULT_FRAME_SIZE,
                                  feature_mode=model.feature,
                                  num_classes=1,
                                  truth_mutex=model.mutex)

            transform_frames = len(audio) // mixture.DEFAULT_FRAME_SIZE
            feature_frames = len(audio) // (mixture.DEFAULT_FRAME_SIZE * fg.decimation * fg.step)

            feature = np.empty((feature_frames, fg.stride, fg.num_bands))
            mock_truth = np.empty(fg.num_classes)

            feature_frame = 0
            for transform_frame in range(transform_frames):
                indices = slice(transform_frame * mixture.DEFAULT_FRAME_SIZE,
                                (transform_frame + 1) * mixture.DEFAULT_FRAME_SIZE)
                fd = fft.execute(int16_to_float(audio[indices]))
                fg.execute(fd, mock_truth)
                if fg.eof():
                    feature[feature_frame] = fg.feature()
                    feature_frame += 1
        elif ext == '.h5':
            with h5py.File(name=input_name, mode='r') as f:
                feature = np.array(f['feature'])
        else:
            raise SonusAIError(f'Unknown file type for {input_name}')

        logger.debug(f'Input shape {feature.shape}')

        predict = model.execute(feature)

        if expect_name:
            with h5py.File(name=expect_name, mode='r') as f:
                expected = np.array(f['predict'])
                logger.debug(f'Expect shape {expected.shape}')
                if expected.shape != predict.shape:
                    raise SonusAIError('Expect shape does not match input shape')

                max_error = np.amax(np.abs(predict - expected))
                logger.info(f'Maximum error = {max_error}')

        if output_name:
            with h5py.File(name=output_name, mode='w') as f:
                f.create_dataset(name='predict', data=predict)
                logger.info(f'Wrote {output_name}')

        end_time = time.monotonic()
        logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
