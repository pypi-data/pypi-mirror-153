from pyaaware import FeatureGenerator

import sonusai


def get_feature_stats(feature_mode: str,
                      frame_size: int,
                      num_classes: int,
                      truth_mutex: bool) -> (float, int, float, int, int, int):
    fg = FeatureGenerator(feature_mode=feature_mode,
                          frame_size=frame_size,
                          num_classes=num_classes,
                          truth_mutex=truth_mutex)
    num_bands = fg.num_bands
    stride = fg.stride
    step = fg.step
    decimation = fg.decimation
    transform_frame_ms = float(frame_size) / float(sonusai.mixture.SAMPLE_RATE / 1000)
    feature_ms = transform_frame_ms * decimation * stride
    feature_step_ms = transform_frame_ms * decimation * step
    feature_samples = frame_size * decimation * stride
    feature_step_samples = frame_size * decimation * step
    return feature_ms, feature_samples, feature_step_ms, feature_step_samples, num_bands, stride
