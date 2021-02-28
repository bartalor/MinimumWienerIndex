from typing import List


class Dot:
    def __init__(self, pos, leaf: bool, special: bool, neighbors: List):
        self.pos = pos
        self.leaf = leaf
        self.special = special
        self.bors = neighbors

    def print_dot(self, dot_list):
        str_index = "index: " + str(dot_list.index(self))
        str_pos = "pos: " + str(self.pos)
        str_leaf = "leaf: " + str(self.leaf)
        str_special = "special: " + str(self.special)
        str_neighbors = "neighbors: \n " + \
            ", ".join([str(dot_list.index(bor)) for bor in self.bors])
        to_print = str_index + "\n" + \
           str_pos + ", " + \
           str_leaf + ", " + \
           str_special + "\n" + \
           str_neighbors + "\n"
        print(to_print)