from typing import Any, Union, Optional, Iterable

from collections import namedtuple

from gymnasium import spaces
import numpy as np
from numpy.typing import NDArray


def gymnasium_space_val_to_key(space_val: Any, space: spaces.Space):
    assert space.contains(space_val), f'observation space {space} does not contain given observationL: {space_val}'

    # fundamental spaces
    if isinstance(space, spaces.Box):
        return box_to_key(space_val)
    elif isinstance(space, spaces.Discrete):
        return discrete_to_key(space_val)
    elif isinstance(space, spaces.Text):
        return text_to_key(space_val)
    elif isinstance(space, spaces.MultiDiscrete):
        return multi_discrete_to_key(space_val)
    elif isinstance(space, spaces.MultiBinary):
        return multi_binary_to_key(space_val)

    # composite spaces
    elif isinstance(space, spaces.Graph):
        return graph_to_key(space_val, space.node_space, space.edge_space)
    elif isinstance(space, spaces.Tuple):
        return tuple_to_key(space_val, space.spaces)
    elif isinstance(space, spaces.Sequence):
        return sequence_to_key(space_val, space.feature_space)
    elif isinstance(space, spaces.Dict):
        return dict_to_key(space_val, space.spaces)

    # unsupported spaces
    else:
        raise ValueError(f'unsupported space type {type(space)}')


######################
# Fundamental Spaces #
######################

def box_to_key(box: NDArray[Any]):
    out = []

    for row in box:  # iterate array rows
        if row.ndim == 1:  # if singleton, return as tuple
            row_key = tuple(row)
        else:  # otherwise, parse recursively
            row_key = box_to_key(row)
        out.append(row_key)

    # return as tuple
    return tuple(out)


def discrete_to_key(discrete: np.int64):
    return discrete


def text_to_key(text: str):
    return text


def multi_discrete_to_key(multi_discrete: NDArray[np.integer[Any]]):
    return tuple(multi_discrete)


def multi_binary_to_key(multi_binary: NDArray[np.int8]):
    return tuple(multi_binary)


####################
# Composite Spaces #
####################

GraphTuple = namedtuple('GraphTuple', 'nodes, edges, edge_links')


def graph_to_key(graph: spaces.GraphInstance, node_space: spaces.Space, edge_space: Optional[spaces.Space]):
    node_keys = []
    for node in graph.nodes:
        node_key = gymnasium_space_val_to_key(node, node_space)
        node_keys.append(node_key)
    nodes_key = tuple(node_keys)

    if graph.edges is not None:
        edge_keys = []
        for edge in graph.edges:
            edge_key = gymnasium_space_val_to_key(edge, node_space)
            edge_keys.append(edge_key)
        edges_key = tuple(edge_keys)
    else:
        edges_key = None

    if graph.edge_links is not None:
        edge_links_key = box_to_key(graph.edge_links)
    else:
        edge_links_key = None

    return GraphTuple(nodes_key, edges_key, edge_links_key)


def tuple_to_key(tuple_: tuple[Any, ...], tuple_spaces: Iterable[spaces.Space[Any]]):
    out = []
    for item, space in zip(tuple_, tuple_spaces):
        item_key = gymnasium_space_val_to_key(item, space)
        out.append(item_key)

    return tuple(out)


def sequence_to_key(sequence: Union[tuple[Any, ...], Any], sequence_space: spaces.Space[Any]):
    sequence = tuple(sequence)  # even if `stacked=True`, always treat as a tuple
    return tuple_to_key(tuple(sequence), [sequence_space] * len(sequence))


def dict_to_key(dict_: dict[str, Any], dict_spaces: dict[str, spaces.Space[Any]]):
    out = {}
    for key, value in dict_.items():
        out[key] = gymnasium_space_val_to_key(value, dict_spaces[key])

    DictTuple = namedtuple(f'DictTuple__{"_".join(out.keys())}', out.keys())
    return DictTuple(**out)
