from typing import List
from Definitions import Dot


def is_leaf(dot: Dot) -> bool:
    return len(dot.bors) == 1


def is_special(dot: Dot) -> bool:
    bors = dot.bors
    leaf_bors_N = sum([x.leaf for x in bors])
    non_leaf_bors_N = len(bors) - leaf_bors_N
    return 0 < leaf_bors_N and non_leaf_bors_N == 1


def copy_dot_list(dot_list: List[Dot]) -> List[Dot]:
    bors_index_list = \
        [[dot_list.index(bor) for bor in dot.bors] for dot in dot_list]
    dot_list_copy = [Dot(dot.pos, dot.leaf, dot.special, []) for dot in dot_list]
    assert len(bors_index_list) == len(dot_list_copy)
    for dot_bors_i, dot in zip(bors_index_list, dot_list_copy):
        dot.bors = [dot_list_copy[i] for i in dot_bors_i]
    return dot_list_copy
