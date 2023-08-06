from typing import Any
from typing import Callable
from typing import List
from typing import Union


def get_mixids_from_mixture_field_predicate(mixdb: dict,
                                            field: str,
                                            mixid: Union[str, List[int]] = None,
                                            predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixture IDs based on mixture field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from sonusai.mixture import convert_mixid_to_list

    mixid_out = convert_mixid_to_list(mixdb, mixid)

    if predicate is None:
        def predicate(x: Any) -> bool:
            return True

    criteria = sorted(
        list(set([x[field] for i, x in enumerate(mixdb['mixtures']) if predicate(x[field]) and i in mixid_out])))

    result = dict()
    for criterion in criteria:
        result[criterion] = [i for i, x in enumerate(mixdb['mixtures']) if x[field] == criterion and i in mixid_out]

    return result


def get_mixids_from_truth_settings_field_predicate(mixdb: dict,
                                                   field: str,
                                                   mixid: Union[str, List[int]] = None,
                                                   predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixture IDs based on target truth_settings field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from sonusai.mixture import convert_mixid_to_list

    mixid_out = convert_mixid_to_list(mixdb, mixid)

    # Get all field values
    values = get_all_truth_settings_values_from_field(mixdb, field)

    if predicate is None:
        def predicate(x: Any) -> bool:
            return True

    # Get only values of interest
    values = [value for value in values if predicate(value)]

    result = dict()
    for value in values:
        # Get a list of targets for each field value
        indices = list()
        for i, target in enumerate(mixdb['targets']):
            for truth_setting in target['truth_settings']:
                if value in truth_setting[field]:
                    indices.append(i)
        indices = sorted(list(set(indices)))

        mixids = list()
        for index in indices:
            mixids.extend([i for i, x in enumerate(mixdb['mixtures']) if
                           x['target_file_index'] == index and i in mixid_out])

        mixids = sorted(list(set(mixids)))
        if mixids:
            result[value] = mixids

    return result


def get_all_truth_settings_values_from_field(mixdb: dict, field: str) -> list:
    """
    Generate a list of all values corresponding to the given field in truth_settings
    """
    result = list()
    for target in mixdb['targets']:
        for truth_setting in target['truth_settings']:
            value = truth_setting[field]
            if isinstance(value, str):
                value = [value]
            result.extend(value)

    return sorted(list(set(result)))


def get_mixids_from_noise(mixdb: dict,
                          mixid: Union[str, List[int]] = None,
                          predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on noise index predicate
    Return a dictionary where:
        - keys are the noise indices
        - values are lists of the mixids that match the noise index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixid=mixid,
                                                   field='noise_file_index',
                                                   predicate=predicate)


def get_mixids_from_noise_augmentation(mixdb: dict,
                                       mixid: Union[str, List[int]] = None,
                                       predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on a noise augmentation index predicate
    Return a dictionary where:
        - keys are the noise augmentation indices
        - values are lists of the mixids that match the noise augmentation index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixid=mixid,
                                                   field='noise_augmentation_index',
                                                   predicate=predicate)


def get_mixids_from_target(mixdb: dict,
                           mixid: Union[str, List[int]] = None,
                           predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on a target index predicate
    Return a dictionary where:
        - keys are the target indices
        - values are lists of the mixids that match the target index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixid=mixid,
                                                   field='target_file_index',
                                                   predicate=predicate)


def get_mixids_from_target_augmentation(mixdb: dict,
                                        mixid: Union[str, List[int]] = None,
                                        predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on a target augmentation index predicate
    Return a dictionary where:
        - keys are the target augmentation indices
        - values are lists of the mixids that match the target augmentation index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixid=mixid,
                                                   field='target_augmentation_index',
                                                   predicate=predicate)


def get_mixids_from_snr(mixdb: dict,
                        mixid: Union[str, List[int]] = None,
                        predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on an SNR predicate
    Return a dictionary where:
        - keys are the SNRs
        - values are lists of the mixids that match the SNR
    """
    from sonusai.mixture import convert_mixid_to_list

    mixid_out = convert_mixid_to_list(mixdb, mixid)

    # Get all the SNRs
    snrs = mixdb['noise_mix']['snrs']

    if predicate is None:
        def predicate(x: Any) -> bool:
            return True

    # Get only the SNRs of interest (filter on predicate)
    snrs = [snr for snr in snrs if predicate(snr)]

    result = dict()
    for snr in snrs:
        # Get a list of mixids for each SNR
        result[snr] = sorted([i for i, x in enumerate(mixdb['mixtures']) if x['snr'] == snr and i in mixid_out])

    return result


def get_mixids_from_truth_index(mixdb: dict,
                                mixid: Union[str, List[int]] = None,
                                predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on a truth index predicate
    Return a dictionary where:
        - keys are the truth indices
        - values are lists of the mixids that match the truth index
    """
    return get_mixids_from_truth_settings_field_predicate(mixdb=mixdb,
                                                          mixid=mixid,
                                                          field='index',
                                                          predicate=predicate)


def get_mixids_from_truth_function(mixdb: dict,
                                   mixid: Union[str, List[int]] = None,
                                   predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on a truth function predicate
    Return a dictionary where:
        - keys are the truth functions
        - values are lists of the mixids that match the truth function
    """
    return get_mixids_from_truth_settings_field_predicate(mixdb=mixdb,
                                                          mixid=mixid,
                                                          field='function',
                                                          predicate=predicate)
