from typing import List
from typing import Union

from sonusai.mixture.get_mixtures_from_mixid import convert_mixid_to_list
from sonusai.mixture.mixture_data import get_feature_frames_in_mixture
from sonusai.mixture.segment import Segment


def get_file_frame_segments(mixdb: dict, mixid: Union[str, List[int]] = ':') -> dict:
    _mixid = convert_mixid_to_list(mixdb, mixid)
    file_frame_segments = dict()
    for m in _mixid:
        file_frame_segments[m] = Segment(mixdb['mixtures'][m]['o_frame_offset'],
                                         get_feature_frames_in_mixture(mixdb, m))
    return file_frame_segments
