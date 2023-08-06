from sonusai.mixture.generate_truth import get_truth_indices_for_target


def get_targets_for_truth_index(mixdb: dict, truth_index: int, allow_multiple: bool = False) -> list:
    """Get a list of targets containing the given truth index.

    If allow_multiple is True, then include targets that contain multiple truth indices.
    """
    target_indices = set()
    for target_index, target in enumerate(mixdb['targets']):
        indices = get_truth_indices_for_target(mixdb, target_index)
        if len(indices) == 1 or allow_multiple:
            for index in indices:
                if index == truth_index + 1:
                    target_indices.add(target_index)

    return sorted(list(target_indices))
