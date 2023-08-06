from glob import glob
from os import listdir
from os.path import dirname
from os.path import isabs
from os.path import isdir
from os.path import join
from os.path import splitext
from typing import List
from typing import Union

import sox

from sonusai import SonusAIError
from sonusai.mixture.config import raw_load_config
from sonusai.utils.expandvars import expandvars


def get_input_files(records: List[dict],
                    truth_settings: Union[List[dict], None] = None) -> List[dict]:
    if truth_settings is None:
        truth_settings = list()

    files = list()
    for record in records:
        append_input_files(files, record, truth_settings)
    return files


def append_input_files(files: List[dict],
                       in_record: Union[dict, str],
                       truth_settings: List[dict],
                       tokens: Union[dict, None] = None) -> None:
    if tokens is None:
        tokens = dict()

    if isinstance(in_record, dict):
        if 'target_name' in in_record:
            in_name = in_record['target_name']
        else:
            raise SonusAIError('Target list contained record without target_name')

        if 'truth_settings' in in_record:
            truth_settings = in_record['truth_settings']
    else:
        in_name = in_record

    in_name, new_tokens = expandvars(in_name)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                append_input_files(files, child, truth_settings, tokens)
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = expandvars(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                append_input_files(files, child, truth_settings, tokens)
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'targets' in yml_config:
                            for record in yml_config['targets']:
                                append_input_files(files, record, truth_settings, tokens)
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    sox.file_info.validate_input_file(name)
                    duration = sox.file_info.duration(name)
                    for key, value in tokens.items():
                        name = name.replace(value, f'${key}')
                    entry = {
                        'name':     name,
                        'duration': duration,
                    }
                    if len(truth_settings) > 0:
                        entry['truth_settings'] = truth_settings
                        for truth_setting in entry['truth_settings']:
                            if 'function' in truth_setting and truth_setting['function'] == 'file':
                                truth_setting['config']['file'] = splitext(name)[0] + '.h5'
                    files.append(entry)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')
