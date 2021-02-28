import math
import time
from itertools import combinations


start_time = time.time()
from Planar_Helper_functions import areCrossing
import networkx as nx

count = 0


def edge_can_be_added(previouslyAddedEdges, myEdge):
    # checks if it intercets with previously added edges
    for previousEdge in previouslyAddedEdges:
        if (areCrossing(myEdge, previousEdge)):
            return False
    return True


def getSuitableNetworkxGraph(previouslyAddedEdges):
    G = nx.Graph()
    for edge in previouslyAddedEdges:
        G.add_edge(edge.node1index, edge.node2index, weight=edge.distance)
    return G




def convertToSimpleList(edgeList):
    result = []
    for edge in edgeList:
        result.append([edge.node1index, edge.node2index, edge.distance])
    return result


def printEdgeList(edgeList):
    print(convertToSimpleList(edgeList))


def getPlanarPlane(vers):
    return add_edges(list(combinations(vers, 2)))


def add_edges(allEdges, previouslyAddedEdges=None):
    if previouslyAddedEdges is None:
        previouslyAddedEdges = []
    edges_without_selfs = \
        [e for e in allEdges if e[0] != e[1]]
    edges_sorted = sorted(edges_without_selfs, key=(lambda arg: math.dist(arg[0], arg[1])))
    for edge in edges_sorted:
        if edge_can_be_added(previouslyAddedEdges, edge):
            previouslyAddedEdges.append(edge)
    return previouslyAddedEdges
