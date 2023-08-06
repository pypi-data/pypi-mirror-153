import json
import random
from copy import copy
from typing import List
from typing import Union

import h5py
import numpy as np
from tensorflow.keras.utils import Sequence

from sonusai import SonusAIError
from sonusai.mixture import Segment
from sonusai.mixture import convert_mixid_to_list
from sonusai.mixture import get_feature_frames_in_mixture
from sonusai.mixture import get_mixtures_from_mixid
from sonusai.utils import reshape_inputs


class DataGenerator(Sequence):
    """Generates data for Keras"""

    def __init__(self,
                 filename: str,
                 mixid: Union[str, List[int]],
                 batch_size: int,
                 timesteps: int,
                 flatten: bool,
                 add1ch: bool,
                 shuffle: bool = False):
        """Initialization"""
        self.filename = filename
        self.mixid = mixid
        self.batch_size = batch_size
        self.timesteps = timesteps
        self.flatten = flatten
        self.add1ch = add1ch
        self.shuffle = shuffle

        try:
            self.file = h5py.File(self.filename, 'r')
            self.mixdb = json.loads(self.file.attrs['mixdb'])
            self.stride = self.file['feature'].shape[1]
            self.num_bands = self.file['feature'].shape[2]
            self.num_classes = self.file['truth_f'].shape[1]
        except Exception as e:
            raise SonusAIError(f'Error: {e}')

        self.mixid = convert_mixid_to_list(self.mixdb, self.mixid)

        self.file_frame_segments = dict()
        for m in self.mixid:
            self.file_frame_segments[m] = Segment(self.mixdb['mixtures'][m]['o_frame_offset'],
                                                  get_feature_frames_in_mixture(self.mixdb, m))

        self.mixtures = None
        self.mixture_frame_segments = None
        self.batch_frame_segments = None
        self.total_batches = None
        self.frames_per_batch = None

        self._initialize_mixtures()

    def __len__(self) -> int:
        """Denotes the number of batches per epoch"""
        return self.total_batches

    def __getitem__(self, batch_index: int) -> (np.ndarray, np.ndarray):
        """Get one batch of data"""
        feature = np.empty((self.frames_per_batch, self.stride, self.num_bands), dtype=np.single)
        truth = np.empty((self.frames_per_batch, self.num_classes), dtype=np.single)
        start = 0
        for segment in self.batch_frame_segments[batch_index]:
            length = segment.length
            feature[start:start + length] = self.file['feature'][segment.get_slice()]
            truth[start:start + length] = self.file['truth_f'][segment.get_slice()]
            start += length

        feature, truth, _, _, _, _ = reshape_inputs(feature=feature,
                                                    truth=truth,
                                                    batch_size=self.batch_size,
                                                    timesteps=self.timesteps,
                                                    flatten=self.flatten,
                                                    add1ch=self.add1ch)
        return feature, truth

    def on_epoch_end(self) -> None:
        """Modification of dataset between epochs"""
        if self.shuffle:
            random.shuffle(self.mixid)
            self.initialize_mixtures()

    def _initialize_mixtures(self) -> None:
        self.mixtures = get_mixtures_from_mixid(self.mixdb, self.mixid)
        self.mixture_frame_segments = [self.file_frame_segments[m] for m in self.mixid]

        frames = sum([sub['samples'] for sub in self.mixtures]) // self.mixdb['feature_step_samples']
        self.frames_per_batch = self.batch_size if self.timesteps == 0 else self.batch_size * self.timesteps
        self.total_batches = frames // self.frames_per_batch

        if self.total_batches == 0:
            raise SonusAIError(
                f'Error: dataset only contains {frames} frames which is not enough to fill a batch size of '
                f'{self.frames_per_batch}. Either provide more data or decrease the batch size')

        # Compute mixid and offset for dataset
        # offsets are needed because mixtures are not guaranteed to fall on batch boundaries.
        # When fetching a new index that starts in the middle of a sequence of mixtures, the
        # previous feature frame offset must be maintained in order to preserve the correct
        # data sequence.
        cumulative_frames = 0
        start_mixture_index = 0
        offset = 0
        index_map = list()
        for m in range(len(self.mixture_frame_segments)):
            current_frames = self.mixture_frame_segments[m].length
            cumulative_frames += current_frames
            while cumulative_frames >= self.frames_per_batch:
                extra_frames = cumulative_frames - self.frames_per_batch
                index_map.append({
                    'mixid':  list(range(start_mixture_index, m + 1)),
                    'offset': offset,
                    'extra':  extra_frames
                })
                if extra_frames == 0:
                    start_mixture_index = m + 1
                    offset = 0
                else:
                    start_mixture_index = m
                    offset = current_frames - extra_frames
                cumulative_frames = extra_frames

        self.batch_frame_segments = list()
        for item in index_map:
            slices = list()
            for m in item['mixid']:
                slices.append(copy(self.mixture_frame_segments[m]))
            slices[0].trim_start(item['offset'])
            slices[-1].trim_length(item['extra'])
            consolidated_segments = list()
            start = slices[0].start
            length = slices[0].length
            for i in range(1, len(slices)):
                if slices[i].start != start + length:
                    consolidated_segments.append(Segment(start, length))
                    start = slices[i].start
                    length = slices[i].length
                else:
                    length += slices[i].length
            consolidated_segments.append(Segment(start, length))

            self.batch_frame_segments.append(consolidated_segments)
