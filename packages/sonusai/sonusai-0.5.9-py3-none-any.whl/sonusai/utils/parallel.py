"""Map functions for parallel processing.

p_map:  Performs a parallel ordered map.
p_umap: Performs a parallel unordered map.
"""

import multiprocessing as mp
from typing import Any
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import List


def initialize_map_func(ordered: bool, **kwargs: Any) -> Callable:
    # Extract num_cpus
    num_cpus = kwargs.pop('num_cpus', None)

    # Determine num_cpus
    if num_cpus is None:
        num_cpus = mp.cpu_count()
    elif type(num_cpus) == float:
        num_cpus = int(round(num_cpus * mp.cpu_count()))

    # Create parallel generator
    initializer = kwargs.pop('initializer', None)
    initargs = kwargs.pop('initargs', None)
    map_type = 'imap' if ordered else 'uimap'
    pool = mp.Pool(num_cpus, initializer=initializer, initargs=initargs)
    map_func = getattr(pool, map_type)

    return map_func


def _parallel(ordered: bool, function: Callable, *iterables: Iterable, **kwargs: Any) -> Generator:
    """Returns a generator for a parallel map.

    Arguments:
        ordered     bool        True for an ordered map, False for an unordered map.
        function    Callable    The function to apply to each element of the given Iterable.
        iterables   Iterable    One or more Iterables containing the data to be mapped.

    Returns:
        A generator which will apply the function to each element of the given Iterables
        in parallel in order.
    """
    map_func = initialize_map_func(ordered, **kwargs)

    for item in map_func(function, *iterables):
        yield item


def p_map(function: Callable, *iterables: Iterable, **kwargs: Any) -> List[Any]:
    """Performs a parallel ordered map."""
    return list(_parallel(True, function, *iterables, **kwargs))


def p_umap(function: Callable, *iterables: Iterable, **kwargs: Any) -> List[Any]:
    """Performs a parallel unordered map."""
    return list(_parallel(False, function, *iterables, **kwargs))
