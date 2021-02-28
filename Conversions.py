import math
from typing import Tuple, List
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree


from Tree.Definitions import Dot
from Tree.Tree_Helper_functions import is_leaf, is_special, copy_dot_list


def networkx_to_outp_format(graph, index, type):
    return {
        "index": index,
        "graph_type": type,
        "wiener_index": nx.wiener_index(graph, weight='weight'),
        "edges": list(graph.edges())
    }


def networkx_to_coors(graph, vers) -> \
        List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    edges = graph.edges
    return [(vers[edge[0]], vers[edge[1]]) for edge in edges]


def edge_coors_to_networkx(edges_coors, vers):
    edges_networkx_format = [(vers.index(edge[0]), vers.index(edge[1]), \
                              (math.dist(edge[0], edge[1]))) for edge in edges_coors]
    Gx = nx.Graph()
    for x in edges_networkx_format:
        Gx.add_edge(x[0], x[1], weight=x[2])
    return Gx


def inp_vers_to_coors(inp):
    return [(elem['x'], elem['y']) for elem in inp["graph_verts"]]


def orig_ver_to_coor(ver) -> Tuple[float, float]:
    return ver["x"], ver["y"]


def coors_to_inp_format(vers):
    return {"graph_verts":
                [{"point_index": i, "x": ver[0], "y": ver[1]}
                 for i,ver in enumerate(vers)]}


def vers_to_mst(vers):
    adj_mat = [[math.dist(ver1, ver2) for ver2 in vers] for ver1 in vers]
    X = csr_matrix(adj_mat)
    Tcsr = minimum_spanning_tree(X)
    mat = Tcsr.toarray().astype(float)
    def fixscipy(matrix):
        length = len(matrix)
        for i in range(length):
            for j in range(length):
                if (j < i):
                    if (matrix[i][j] == 0):
                        matrix[i][j] = matrix[j][i]
                    if (matrix[j][i] == 0):
                        matrix[j][i] = matrix[i][j]
        return matrix
    return fixscipy(mat)


def mst_adj_mat_to_dot_list(adj_mat, vers):
    # print(adj_mat)
    adj_list = [[i for i, y in enumerate(x) if y] for x in adj_mat]
    dot_list = [Dot(pos, False, False, []) for pos in vers]
    # initialize neighbors:
    assert len(dot_list) == len(adj_list)
    for dot_bors_i, dot in zip(adj_list, dot_list):
        dot.bors = [dot_list[i] for i in dot_bors_i]
    # initialize leaves ** requires that neighbors are initialized ** :
    for dot in dot_list:
        dot.leaf = is_leaf(dot)
    # initialize special ** requires that leaves are initialized ** :
    for dot in dot_list:
        dot.special = is_special(dot)

    return dot_list


def networkx_to_dot_list(mst, vers):
    adj_mat = nx.to_numpy_matrix(mst).tolist()
    adj_list = [[i for i, y in enumerate(x) if y] for x in adj_mat]
    dot_list = [Dot(pos, False, False, []) for pos in vers]
    # initialize neighbors:
    assert len(dot_list) == len(adj_list)
    for dot_bors_i, dot in zip(adj_list, dot_list):
        dot.bors = [dot_list[i] for i in dot_bors_i]
    # initialize leaves ** requires that neighbors are initialized ** :
    for dot in dot_list:
        dot.leaf = is_leaf(dot)
    # initialize special ** requires that leaves are initialized ** :
    for dot in dot_list:
        dot.special = is_special(dot)

    return dot_list


def dot_list_to_coors(dot_list: List[Dot]) -> \
        Tuple[Tuple[float, float], Tuple[float, float]]:
    edges = []
    list_copy = copy_dot_list(dot_list)
    for dot in list_copy:
        while dot.bors:
            bor = dot.bors[0]
            edges.append((dot.pos, bor.pos))
            ind = bor.bors.index(dot)
            bor.bors.pop(ind)
            dot.bors.pop(0)
    return edges


