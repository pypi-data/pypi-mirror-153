from copy import deepcopy

import yaml

import sonusai
from sonusai import SonusAIError


def raw_load_config(name: str) -> dict:
    """Load YAML file with SonusAI variable substitution."""
    with open(file=name, mode='r') as f:
        config = yaml.safe_load(f)

    config_variable_substitution(config)
    return config


def config_variable_substitution(config: dict) -> None:
    """Find custom SonusAI variables in given dictionary and substitute their values in place."""
    for key, value in config.items():
        if isinstance(value, dict):
            config_variable_substitution(value)
        else:
            if value == '${frame_size}':
                config[key] = sonusai.mixture.DEFAULT_FRAME_SIZE
            elif isinstance(value, list):
                for idx in range(len(value)):
                    if isinstance(value[idx], str):
                        value[idx] = value[idx].replace('${default_noise}', sonusai.mixture.DEFAULT_NOISE)


def get_default_config() -> dict:
    """Load default SonusAI config."""
    try:
        return raw_load_config(sonusai.mixture.DEFAULT_CONFIG)
    except Exception as e:
        raise SonusAIError(f'Error loading default config: {e}')


def load_config(name: str) -> dict:
    """Load SonusAI default config and update with given YAML file (performing SonusAI variable substitution)."""
    return update_config_from_file(name=name, config=get_default_config())


def update_config_from_file(name: str, config: dict) -> dict:
    """Update the given config with the config in the given YAML file."""
    new_config = deepcopy(config)

    try:
        given_config = raw_load_config(name)
    except Exception as e:
        raise SonusAIError(f'Error loading config from {name}: {e}')

    # Use default config as base and overwrite with given config keys as found
    for key in new_config:
        if key in given_config:
            if key not in ['noise_mix', 'truth_settings']:
                new_config[key] = given_config[key]

    # Handle 'noise_mix' special case
    if 'noise_mix' in given_config:
        new_config['noise_mix'] = deepcopy(given_config['noise_mix'])
    default = deepcopy(config['noise_mix'])
    update_noise_mix(new_config['noise_mix'], default)

    # Handle 'truth_settings' special case
    if 'truth_settings' in given_config:
        new_config['truth_settings'] = deepcopy(given_config['truth_settings'])

    if not isinstance(new_config['truth_settings'], list):
        new_config['truth_settings'] = [new_config['truth_settings']]

    default = deepcopy(config['truth_settings'])
    if not isinstance(default, list):
        default = [default]

    update_truth_settings(new_config['truth_settings'], default)

    # Check for required keys
    required_keys = [
        'class_labels',
        'class_weights_threshold',
        'feature',
        'frame_size',
        'noise_mix',
        'num_classes',
        'seed',
        'targets',
        'target_augmentations',
        'class_balancing_augmentation',
        'truth_settings',
        'truth_mode',
        'truth_reduction_function',
    ]
    for key in required_keys:
        if key not in new_config:
            raise SonusAIError(f"Missing required '{key}' in {name}")

    return new_config


def update_noise_mix(given: dict, default: dict = None) -> None:
    """Update missing fields in given 'noise_mix' with default values."""
    required_keys = [
        'files',
        'augmentations',
        'snrs',
        'exhaustive',
    ]
    for key in required_keys:
        if key not in given:
            if default is not None and key in default:
                given[key] = default[key]
            else:
                raise SonusAIError(f"Missing required '{key}' in noise_mix")

    if not given['snrs']:
        given['snrs'] = [99]


def update_truth_settings(given: list, default: list = None) -> None:
    """Update missing fields in given 'truth_settings' with default values."""
    if default is not None and len(given) != len(default):
        raise SonusAIError(f'Length of truth_settings does not match given default')

    required_keys = [
        'function',
        'config',
        'index',
    ]
    for n in range(len(given)):
        for key in required_keys:
            if key not in given[n]:
                if default is not None and key in default[n]:
                    given[n][key] = default[n][key]
                else:
                    raise SonusAIError(f"Missing required '{key}' in truth_settings")


def get_hierarchical_config_files(root: str, leaf: str) -> list:
    """Get a hierarchical list of config files in the given leaf of the given root."""
    import os
    from pathlib import Path

    config_file = 'config.yml'

    root_path = Path(os.path.abspath(root))
    if not root_path.is_dir():
        raise SonusAIError(f'Given root, {root_path}, is not a directory.')

    leaf_path = Path(os.path.abspath(leaf))
    if not leaf_path.is_dir():
        raise SonusAIError(f'Given leaf, {leaf_path}, is not a directory.')

    common = os.path.commonpath((root_path, leaf_path))
    if os.path.normpath(common) != os.path.normpath(root_path):
        raise SonusAIError(f'Given leaf, {leaf_path}, is not in the hierarchy of the given root, {root_path}')

    top_config_file = Path(os.path.join(root_path, config_file))
    if not top_config_file.is_file():
        raise SonusAIError(f'Could not find {top_config_file}')

    current = leaf_path
    config_files = list()
    while current != root_path:
        local_config_file = Path(os.path.join(current, config_file))
        if local_config_file.is_file():
            config_files.append(local_config_file)
        current = current.parent

    config_files.append(top_config_file)
    return list(reversed(config_files))


def update_config_from_hierarchy(root: str, leaf: str, config: dict) -> dict:
    """Update the given config using the hierarchical config files in the given leaf of the given root."""
    new_config = deepcopy(config)
    config_files = get_hierarchical_config_files(root=root, leaf=leaf)
    for config_file in config_files:
        new_config = update_config_from_file(name=config_file, config=new_config)

    return new_config


def get_max_class(num_classes: int, truth_mutex: bool) -> int:
    """Get the maximum class index."""
    max_class = num_classes
    if truth_mutex:
        max_class -= 1
    return max_class
