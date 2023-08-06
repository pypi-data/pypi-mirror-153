from typing import List
from typing import Union


def convert_mixid_to_list(mixdb: dict, mixid: Union[str, List[int]] = None) -> List[int]:
    mixid_out = mixid

    if mixid_out is None:
        return list(range(len(mixdb['mixtures'])))

    if isinstance(mixid_out, str):
        try:
            mixid_out = list(eval(f'range(len({mixdb["mixtures"]}))[{mixid_out}]'))
        except NameError:
            return []

    if not all(isinstance(x, int) and x < len(mixdb['mixtures']) for x in mixid_out):
        return []

    return mixid_out


def get_mixtures_from_mixid(mixdb: dict, mixid: Union[str, List[int]] = None) -> list:
    mixid_out = convert_mixid_to_list(mixdb, mixid)

    return [mixdb['mixtures'][i] for i in mixid_out]
