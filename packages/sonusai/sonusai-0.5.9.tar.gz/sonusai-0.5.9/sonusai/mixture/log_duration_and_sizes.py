import sonusai
from sonusai import logger
from sonusai.utils.human_readable_size import human_readable_size
from sonusai.utils.seconds_to_hms import seconds_to_hms


def log_duration_and_sizes(total_duration: int,
                           num_classes: int,
                           feature_step_samples: int,
                           num_bands: int,
                           stride: int,
                           desc: str) -> None:
    total_samples = total_duration * sonusai.mixture.SAMPLE_RATE
    mixture_bytes = total_samples * sonusai.mixture.BIT_DEPTH / 8
    truth_t_bytes = total_samples * num_classes * sonusai.mixture.FLOAT_BYTES
    feature_bytes = total_samples / feature_step_samples * stride * num_bands * sonusai.mixture.FLOAT_BYTES
    truth_f_bytes = total_samples / feature_step_samples * num_classes * sonusai.mixture.FLOAT_BYTES

    logger.info('')
    logger.info(f'{desc} duration:   {seconds_to_hms(seconds=total_duration)}')
    logger.info('{desc} sizes:')
    logger.info(f' mixture:             {human_readable_size(mixture_bytes, 1)}')
    logger.info(f' truth_t:             {human_readable_size(truth_t_bytes, 1)}')
    logger.info(f' feature:             {human_readable_size(feature_bytes, 1)}')
    logger.info(f' truth_f:             {human_readable_size(truth_f_bytes, 1)}')
