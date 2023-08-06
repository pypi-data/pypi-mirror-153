from typing import List


def load_mixid(mixdb: dict, name: str = None) -> List[int]:
    import json
    from os.path import exists

    from sonusai import SonusAIError

    if name is None:
        mixid = list(range(len(mixdb['mixtures'])))
    else:
        if not exists(name):
            raise SonusAIError(f'{name} does not exist')

        with open(file=name, mode='r', encoding='utf-8') as f:
            mixid = json.load(f)
            if not isinstance(mixid, dict) or 'mixid' not in mixid:
                raise SonusAIError(f'Could not find ''mixid'' in {name}')
            mixid = mixid['mixid']

    return mixid
