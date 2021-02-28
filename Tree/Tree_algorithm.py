import math
from typing import *
from Conversions import  dot_list_to_coors, edge_coors_to_networkx, \
    inp_vers_to_coors,  vers_to_mst, mst_adj_mat_to_dot_list
from Tree.Definitions import Dot
from Tree.Tree_Helper_functions import is_leaf, is_special

debug = 1


def print1(strng):
    if 0 < debug:
        print(strng)


def print2(strng):
    if 1 < debug:
        print(strng)


def tree_algorithm(vers) -> List:
    mst = vers_to_mst(vers)
    print1("finished making mst!")
    dots = mst_adj_mat_to_dot_list(mst, vers)
    print1("finished making dot list from networkx mst!")
    improve_mst(dots)
    res = dot_list_to_coors(dots)
    return edge_coors_to_networkx(res, vers)


def improve_mst(dots: List[Dot]):
    print1("finished converting start improving!")
    N = len(dots)
    limit = math.inf
    total_modified = 0
    modified = 1
    while 0 < modified and 0 < limit:
        modified = 0
        for cur_dot in dots:
            bors = cur_dot.bors
            limit -= 1
            if cur_dot.special:
                grampa = next((x for x in bors if not x.leaf), None)
                bors_copy = [bor for bor in bors]
                bors_copy.remove(grampa)
                kids = bors_copy
                rest_N = N - 1 - len(kids)
                modified += alter_special(cur_dot, grampa, kids, rest_N)
                if 0 < modified:
                    print2("modified: " + str(modified))
                total_modified += modified


#  alter_special function important remarks:
#  rest_N includes grampa
def alter_special(dad: Dot, grampa: Dot, kids: List[Dot], rest_N):
    modified = False
    kids_sorted = sorted(kids, key=lambda kid: math.dist(kid.pos, grampa.pos))
    alter_N = count_alter(dad, grampa, kids_sorted, rest_N)
    if 0 < alter_N:
        modified = True
    to_alter = kids_sorted[:alter_N]
    for kid in to_alter:
        # disconnecting kid from dad:
        kid.bors.pop()
        dad.bors.remove(kid)

        # connecting kid to grampa:
        kid.bors.append(grampa)
        grampa.bors.append(kid)

    if is_leaf(dad):
        dad.leaf = True
        dad.special = False
    grampa.special = is_special(grampa)
    return modified


def count_alter(dad: Dot, grampa: Dot, kids: List[Dot], rest_N):
    cur_kids = []
    rest_kids = list.copy(kids)
    best_count = 0
    max_diff = 0
    while len(cur_kids) < len(kids):
        cur_kids.append(rest_kids.pop(0))
        cur_diff = \
            calculate_diff(dad.pos, grampa.pos,
                           [kid.pos for kid in cur_kids],
                           [kid.pos for kid in rest_kids], rest_N)
        if max_diff < cur_diff:
            max_diff = cur_diff
            best_count = len(cur_kids)
    return best_count


# if positive result then alter, else not.
def calculate_diff(dad, grampa, cur_kids, rest_kids, rest_N):
    diff = 0
    # positive:
    # rest_N to cur kids:
    temp_diff = 0
    for kid in cur_kids:
        temp_diff += math.dist(kid, dad) + math.dist(dad, grampa) - math.dist(kid, grampa)
    diff += rest_N * temp_diff

    # negative:
    #  cur_kids to dad
    for kid in cur_kids:
        diff += math.dist(kid, dad) - math.dist(kid, grampa) - math.dist(grampa, dad)

    # cur_kids to rest_kids
    for cur_kid in cur_kids:
        for rest_kid in rest_kids:
            diff += math.dist(cur_kid, dad) - \
                    math.dist(cur_kid, grampa) - \
                    math.dist(grampa, dad)

    return diff
