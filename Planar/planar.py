from scipy.spatial import ConvexHull
from Conversions import edge_coors_to_networkx
from Planar_Algorithm import getPlanarPlane, add_edges


def planar_algorithm(vers, section_size=200):
    vers_sorted = sorted(vers, key=(lambda arg: arg[0]))
    secs = split_arr(vers_sorted, section_size)
    secs_res = [getPlanarPlane(sec) for sec in secs]
    cons = connect_secs(secs_res,secs)
    res = sum(secs_res, []) + cons
    return edge_coors_to_networkx(res,vers)


def connect_secs(secs_edges, secs_vers):
    cons_list = []
    secs_hull_vers = [get_points_on_convex_hull(vers) for vers in secs_vers]
    for i in range(1, len(secs_hull_vers)):
        curr = secs_hull_vers[i]
        prev = secs_hull_vers[i-1]
        edges_to_add = [(ver1,ver2) for ver1 in prev for ver2 in curr]
        prev_edges = secs_edges[i-1] + secs_edges[i]
        if 1 < i:
            prev_edges += cons_list[-1]
        cons_list.append(add_edges(edges_to_add,prev_edges))
    return sum(cons_list, [])


def split_arr(vers, section_size):
    # split:
    splitted = [vers[i:i + section_size] for i in range(0, len(vers), section_size)]
    # check for edge case:
    for i in range(1,len(splitted)):
        assert (splitted[i-1][-1])[0] < (splitted[i][0])[0]
    # add bridge:
    for i in range(1,len(splitted)):
        splitted[i].insert(0,splitted[i-1][-1])
    return splitted


def get_points_on_convex_hull(vers):
    hull = ConvexHull(vers)
    return [vers[i] for i in hull.vertices]