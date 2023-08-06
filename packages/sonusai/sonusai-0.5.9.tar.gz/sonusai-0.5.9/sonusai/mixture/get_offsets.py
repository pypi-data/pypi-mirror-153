from sonusai import SonusAIError


def get_offsets(mixdb: dict, mixid: int) -> (int, int, int):
    required_keys = [
        'mixtures',
        'frame_size',
        'feature_step_samples',
    ]
    for key in required_keys:
        if key not in mixdb:
            raise SonusAIError(f'Missing {key} in mixdb')

    if mixid >= len(mixdb['mixtures']) or mixid < 0:
        raise SonusAIError(f'Invalid mixid: {mixid}')

    i_sample_offset = sum([sub['samples'] for sub in mixdb['mixtures'][:mixid]])
    i_frame_offset = i_sample_offset // mixdb['frame_size']
    o_frame_offset = i_sample_offset // mixdb['feature_step_samples']

    return i_sample_offset, i_frame_offset, o_frame_offset
