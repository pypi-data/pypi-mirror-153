"""sonusai gentcst

usage: gentcst [-hvru] [-o OUTPUT] [-f FOLD] [-y ONTOLOGY]

options:
    -h, --help
    -v, --verbose                       Be verbose.
    -o OUTPUT, --output OUTPUT          Output file name.
    -f FOLD, --fold FOLD                Fold(s) to include. [default: *].
    -y ONTOLOGY, --ontology ONTOLOGY    Reference ontology JSON file for cross-check and adding metadata. [default: ontology.json].
    -r, --hierarchical                  Generate hierarchical multiclass truth for non-leaf nodes.
    -u, --update                        Write JSON metadata into the tree.

Generate a target SonusAI configuration file from a hierarchical subdirectory tree
under the local directory. Leaves in the subdirectory tree define classes by providing SonusAI list
.txt files for class data and additional truth config definitions. This offers a way to simplify and
more clearly manage hierarchical class structure similar to the Audioset ontology.

Features:
    - automatically compiles the target configuration with the number of classes and each truth
      index and the associated files (note: files should use absolute path with env variable)
    - supports hierarchical multilabel class truth generation, where higher nodes in the tree
      are included with leaf truth index, and different leaves with the same name will have the
      same index (i.e. door/squeak, chair/squeak, and brief-tone/squeak)
    - support config overrides for class config.yml or filename.yml for specific file config
    - manages folds via file prefix naming convention, i.e. 1-*.txt, 2-*.txt, etc.
      specifies data for fold 1, 2, etc.
    - cross-check node definitions with the reference ontology and auto copy class metadata into
      the tree to help define/collect data
    - class label is also generated (in the .yml or referencing a .csv)

Inputs:
    The local subdirectory tree with expected top-level configuration file config.yml. This
    file must at least define the feature and can have additional parameters treated as default
    (for truth, augmentation, etc.) which will be included in the generated output yaml file.
    An entire class dataset config parameter can be overridden by including it in a config.yml
    file in the class subdirectory. Individual file config parameters can be further overridden
    or specified in a file of the same name but with .yml (i.e. 1-data.yml with the 1-data.txt)

Outputs:
    output.yml
    output.csv
    gentcst.log

"""
import csv
import json
import os
import re
from copy import deepcopy
from os import getcwd
from os.path import basename
from os.path import dirname
from os.path import exists
from os.path import splitext

import numpy as np
import sh
import yaml
from docopt import docopt

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import get_default_config
from sonusai.mixture import raw_load_config
from sonusai.mixture import update_config_from_hierarchy
from sonusai.mixture import update_truth_settings
from sonusai.utils import trim_docstring

CONFIG_FILE = 'config.yml'


def gentcst(fold: str = '*',
            ontology: str = 'ontology.json',
            hierarchical: bool = False,
            update: bool = False,
            verbose: bool = False) -> (dict, dict):
    update_console_handler(verbose)
    initial_log_messages('gentcst')

    if update:
        logger.info('Updating tree with JSON metadata')
        logger.info('')

    logger.debug(f'fold:         {fold}')
    logger.debug(f'ontology:     {ontology}')
    logger.debug(f'hierarchical: {hierarchical}')
    logger.debug(f'update:       {update}')
    logger.debug('')

    config = get_config()

    if config['truth_mode'] == 'mutex' and hierarchical:
        raise SonusAIError('Multi-class truth is incompatible with truth_mode mutex')

    all_files = get_all_files(hierarchical)
    all_folds = get_folds_from_files(all_files)
    use_folds = get_use_folds(all_folds, fold)
    use_files = get_files_from_folds(all_files, use_folds)
    report_leaf_fold_data_usage(all_files, use_files)

    ontology_data = validate_ontology(ontology, use_files)

    labels = get_labels_from_files(all_files)
    logger.debug('Truth indices:')
    for item in labels:
        logger.debug(f' {item["index"]:3} {item["display_name"]}')
    logger.debug('')

    gen_truth_indices(use_files, labels)

    config['num_classes'] = len(labels)
    if config['truth_mode'] == 'mutex':
        config['num_classes'] = config['num_classes'] + 1

    config['targets'] = []

    logger.info(f'gentcst {len(use_files)} entries in tree')
    root = os.getcwd()
    for file in use_files:
        leaf = dirname(file['file'])
        local_config = get_default_config()
        local_config = update_config_from_hierarchy(root=root, leaf=leaf, config=local_config)
        if not isinstance(local_config['truth_settings'], list):
            local_config['truth_settings'] = [local_config['truth_settings']]

        specific_name = splitext(file['file'])[0] + '.yml'
        if exists(specific_name):
            specific_config = raw_load_config(specific_name)

            for key in specific_config:
                if key != 'truth_settings':
                    local_config[key] = specific_config[key]
                else:
                    if not isinstance(specific_config['truth_settings'], list):
                        specific_config['truth_settings'] = [specific_config['truth_settings']]
                    update_truth_settings(given=specific_config['truth_settings'],
                                          default=local_config['truth_settings'])
                    local_config['truth_settings'] = specific_config['truth_settings']

        truth_settings = deepcopy(local_config['truth_settings'])
        for idx, val in enumerate(truth_settings):
            val['index'] = file['truth_index']
            for key in ['function', 'config']:
                if key in val and val[key] == config['truth_settings'][idx][key]:
                    del val[key]

        target = {
            'target_name':    file['file'],
            'truth_settings': truth_settings
        }

        config['targets'].append(target)

        if update:
            write_metadata_to_tree(ontology_data, file)

    return config, labels


def get_ontology(ontology: str) -> list:
    ontology_data = []

    if exists(ontology):
        with open(file=ontology, mode='r', encoding='utf-8') as f:
            ontology_data = json.load(f)

    # Convert names to lowercase, convert spaces to '-', split into lists on ','
    for item in ontology_data:
        name = item['name'].lower()
        # Need to find ', ' before converting spaces so that we don't convert ', ' to ',-'
        name = name.replace(', ', ',')
        name = name.replace(' ', '-')
        name = name.split(',')
        item['name'] = name

    return ontology_data


def get_dirs() -> list:
    match = sh.find('.', '-type', 'd')
    match = list(map(str.strip, match))

    dirs = []
    for m in match:
        if not m.startswith('./gentcst') and m != '.':
            classes = m.split('/')
            # Remove first element because it is '.'
            classes.pop(0)

            dirs.append({'file': m, 'classes': classes})

    return dirs


def get_leaf_from_classes(classes: list) -> str:
    return '/'.join(classes)


def get_all_files(hierarchical: bool) -> list:
    match = sh.find('.', '-regex', '.*/[0-9]+-.*\.txt')
    match = list(map(str.strip, match))

    files = []
    fold_pattern = re.compile('.*/(\d+)-.*\.txt')
    for m in match:
        fold_match = fold_pattern.match(m)
        if fold_match:
            fold = int(fold_match.group(1))

            classes = m.split('/')
            # Remove first element because it is '.'
            classes.pop(0)
            # Remove last element because it is the file name
            classes.pop()

            leaf = get_leaf_from_classes(classes)

            if hierarchical:
                labels = classes
            else:
                labels = [leaf]

            files.append({'file': m, 'classes': classes, 'leaf': leaf, 'labels': labels, 'fold': fold})

    return files


def get_use_folds(all_folds: list, fold: str) -> list:
    req_folds = get_req_folds(all_folds, fold)
    use_folds = list(set(req_folds).intersection(all_folds))

    logger.debug('Fold information')
    logger.debug(f' Available: {all_folds}')
    logger.debug(f' Requested: {req_folds}')
    logger.debug(f' Used:      {use_folds}')
    logger.debug(f' Unused:    {list(set(use_folds).symmetric_difference(all_folds))}')
    logger.debug(f' Missing:   {list(np.setdiff1d(req_folds, all_folds))}')
    logger.debug('')

    return use_folds


def get_files_from_folds(files: list, folds: list) -> list:
    use_files = []
    for item in files:
        if item['fold'] in folds:
            use_files.append(item)
    return use_files


def get_item_from_name(ontology_data: list, name: str) -> dict:
    return next((item for item in ontology_data if name in item['name']), None)


def get_item_from_id(ontology_data: list, identity: str) -> dict:
    return next((item for item in ontology_data if item['id'] == identity), None)


def get_name_from_id(ontology_data: list, identity: str) -> list:
    name = None
    found = False

    for item in ontology_data:
        if item['id'] == identity:
            if found:
                raise SonusAIError(f'id {identity} appears multiple times in ontology')

            name = item['name']
            found = True

    return name


def get_id_from_name(ontology_data: list, name: str) -> str:
    identity = None
    found = False

    for item in ontology_data:
        if name in item['name']:
            if found:
                raise SonusAIError(f'name {name} appears multiple times in ontology')

            identity = item['id']
            found = True

    return identity


def is_valid_name(ontology_data: list, name: str) -> bool:
    for item in ontology_data:
        if name in item['name']:
            return True
    return False


def is_valid_child(ontology_data: list, parent: str, child: str) -> bool:
    valid = False
    parent_item = get_item_from_name(ontology_data, parent)
    child_id = get_id_from_name(ontology_data, child)

    if child_id is not None and parent_item is not None:
        if child_id in parent_item['child_ids']:
            valid = True

    return valid


def is_valid_hierarchy(ontology_data: list, classes: list) -> bool:
    valid = True

    for parent, child in zip(classes, classes[1:]):
        if not is_valid_child(ontology_data, parent, child):
            valid = False

    return valid


def validate_class(ontology_data: list, file: dict) -> bool:
    valid = True
    classes = file['classes']

    for c in classes:
        if not is_valid_name(ontology_data, c):
            logger.warning(f' Could not find {c} in ontology for {file["file"]}')
            valid = False

    if valid:
        if not is_valid_hierarchy(ontology_data, classes):
            logger.warning(f' Invalid parent/child relationship for {file["file"]}')
            valid = False

    return valid


def expand_range(s: str) -> list:
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l, h = map(int, i.split('-'))
            r += range(l, h + 1)
    return r


def get_req_folds(folds: list, fold: str) -> list:
    if fold == '*':
        return folds

    return expand_range(fold)


def get_folds_from_files(files: list) -> list:
    result = [sub['fold'] for sub in files]
    # Converting to set and back to list ensures uniqueness
    return sorted(list(set(result)))


def get_leaves_from_files(files: list) -> list:
    result = [sub['leaf'] for sub in files]
    # Converting to set and back to list ensures uniqueness
    return sorted(list(set(result)))


def get_labels_from_files(files: list) -> list:
    all_labels = [file['labels'] for file in files]

    # Get labels by depth
    labels_by_depth = [[] for n in range(max([len(label) for label in all_labels]))]
    for label in all_labels:
        for index, name in enumerate(label):
            labels_by_depth[index].append(name)

    for n in range(len(labels_by_depth)):
        # Converting to set and back to list ensures uniqueness
        labels_by_depth[n] = sorted(list(set(labels_by_depth[n])))

    # We want the deepest leaves first
    labels_by_depth.reverse()

    # Now flatten the list
    labels_by_depth = [item for sublist in labels_by_depth for item in sublist]

    # Generate index, name pairs
    labels = []
    for index, file in enumerate(labels_by_depth):
        labels.append({'index': index + 1, 'display_name': file})

    return labels


def gen_truth_indices(files: list, labels: list):
    for file in files:
        file['truth_index'] = []
        for label in file['labels']:
            file['truth_index'].append(get_index_from_label(labels, label))
        file['truth_index'] = sorted(file['truth_index'])


def get_index_from_label(labels: list, label: str) -> int:
    return next((item for item in labels if item['display_name'] == label), None)['index']


def get_config() -> dict:
    if not exists(CONFIG_FILE):
        raise SonusAIError(f'No {CONFIG_FILE} at top level')

    config = raw_load_config(CONFIG_FILE)

    if 'feature' not in config:
        raise SonusAIError('feature not in top level config')

    if 'truth_mode' not in config:
        raise SonusAIError('truth_mode not in top level config')

    if config['truth_mode'] not in ['normal', 'mutex']:
        raise SonusAIError('Invalid truth_mode in top level config')

    if 'truth_settings' in config and not isinstance(config['truth_settings'], list):
        config['truth_settings'] = [config['truth_settings']]

    return config


def validate_ontology(ontology: str, files: list) -> list:
    if exists(ontology):
        ontology_data = get_ontology(ontology)
        logger.debug(f'Reference ontology in {ontology} has {len(ontology_data)} classes')
        logger.debug('')

        logger.info('Checking tree against reference ontology')
        all_dirs = get_dirs()
        valid = True
        for file in all_dirs:
            if not validate_class(ontology_data, file):
                valid = False
        if valid:
            logger.info('PASS')
        logger.info('')

        logger.info('Checking files against reference ontology')
        valid = True
        for file in files:
            if not validate_class(ontology_data, file):
                valid = False
        if valid:
            logger.info('PASS')
        logger.info('')

        return ontology_data

    return []


def get_node_from_name(ontology_data: list, name: str) -> dict:
    nodes = [item for item in ontology_data if name in item['name']]
    if len(nodes) == 1:
        return nodes[0]

    if nodes:
        logger.warning(f'Found multiple entries in reference ontology that match {name}')
    else:
        logger.warning(f'Could not find entry for {name} in reference ontology')

    return {}


def write_metadata_to_tree(ontology_data: list, file: dict):
    if ontology_data:
        node = get_node_from_name(ontology_data, file['classes'][-1])
        if node:
            dir_name = dirname(file['file'])
            json_name = dir_name + '/' + basename(dir_name) + '.json'
            with open(file=json_name, mode='w') as f:
                json.dump(node, f)


def get_folds_from_leaf(all_files: list, leaf: str) -> list:
    files = [item for item in all_files if item['leaf'] == leaf]
    return get_folds_from_files(files)


def report_leaf_fold_data_usage(all_files: list, use_files: list):
    use_leaves = get_leaves_from_files(use_files)
    all_leaves = get_leaves_from_files(all_files)

    logger.debug('Data folds present in each leaf')
    leaf_len = len(max(all_leaves, key=len))
    for leaf in all_leaves:
        folds = get_folds_from_leaf(all_files, leaf)
        logger.debug(f' {leaf:{leaf_len}} {folds}')
    logger.debug('')

    dif_leaves = set(all_leaves).symmetric_difference(use_leaves)
    if dif_leaves:
        logger.warning('This fold selection is missing data from the following leaves')
        for c in dif_leaves:
            logger.warning(f' {c}')
        logger.warning('')


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        output_name = args['--output']
        fold = args['--fold']
        ontology = args['--ontology']
        hierarchical = args['--hierarchical']
        update = args['--update']

        if not output_name:
            output_name = basename(getcwd()) + '.yml'

        log_name = 'gentcst.log'

        create_file_handler(log_name)

        config, labels = gentcst(fold=fold,
                                 ontology=ontology,
                                 hierarchical=hierarchical,
                                 update=update,
                                 verbose=verbose)

        with open(file=output_name, mode='w') as f:
            yaml.dump(config, f)
            logger.info(f'Wrote config to {output_name}')

        csv_fields = ['index', 'display_name']
        csv_name = splitext(output_name)[0] + '.csv'

        with open(file=csv_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields)
            writer.writeheader()
            writer.writerows(labels)
            logger.info(f'Wrote labels to {csv_name}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
