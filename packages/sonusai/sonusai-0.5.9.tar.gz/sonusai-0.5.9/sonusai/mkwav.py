"""sonusai mkwav

usage: mkwav [-hvn] FILE...

options:
   -h, --help
   -v, --verbose        Be verbose.
   -n, --dry-run        Don't actually create files, just show what will be done.

The mkwav command creates WAV files from audio data contained in genft .h5 files.
Specifically, it looks for these datasets: target, noise, and mixture.

"""
import wave
from os.path import splitext

import h5py
from docopt import docopt

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import mixture
from sonusai import update_console_handler
from sonusai.utils import trim_docstring


def mkwav(files: list, dry_run: bool = False, verbose: bool = False):
    update_console_handler(verbose)
    initial_log_messages('mkwav')

    audio_names = ['target', 'noise', 'mixture']

    if dry_run:
        logger.info('Dry run')

    for file in files:
        base_name = splitext(file)[0]
        if verbose:
            logger.info(f'Processing {file}')
        try:
            with h5py.File(file, 'r') as f:
                for audio_name in audio_names:
                    if audio_name in f:
                        out_name = base_name + '_' + audio_name + '.wav'
                        audio = f['/' + audio_name][:]
                        if verbose:
                            logger.info(f'Writing {len(audio)} samples to {out_name}')
                        if not dry_run:
                            with wave.open(out_name, mode='w') as w:
                                w.setnchannels(mixture.CHANNEL_COUNT)
                                w.setsampwidth(mixture.SAMPLE_BYTES)
                                w.setframerate(mixture.SAMPLE_RATE)
                                w.writeframesraw(audio)
        except Exception as e:
            logger.error(f'Error processing {file}: {e}')


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        log_name = 'mkwav.log'
        create_file_handler(log_name)

        files = args['FILE']
        if not isinstance(files, list):
            files = [files]

        mkwav(files=files, dry_run=args['--dry-run'], verbose=args['--verbose'])

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
