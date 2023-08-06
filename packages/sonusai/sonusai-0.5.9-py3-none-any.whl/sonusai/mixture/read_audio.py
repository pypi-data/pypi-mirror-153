from os.path import expandvars

import numpy as np
import sox

from sonusai import SonusAIError
from sonusai import logger
from sonusai.mixture.constants import BIT_DEPTH
from sonusai.mixture.constants import CHANNEL_COUNT
from sonusai.mixture.constants import SAMPLE_RATE


def read_audio(name: str) -> np.ndarray:
    expanded_name = expandvars(name)

    try:
        # Read in and convert to desired format
        inp = sox.Transformer()
        inp.set_output_format(rate=SAMPLE_RATE, bits=BIT_DEPTH, channels=CHANNEL_COUNT)
        return inp.build_array(input_filepath=expanded_name,
                               sample_rate_in=int(sox.file_info.sample_rate(expanded_name)))

    except Exception as e:
        if name != expanded_name:
            logger.error(f'Error reading {name} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {name}: {e}')
