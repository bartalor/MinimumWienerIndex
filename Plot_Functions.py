from typing import *
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import collections as mc


radius: int = 9
plot_dpi: int = 2000
fig = plt.gcf()


def make_vers(vers: List[Tuple[float, float]]):
    coord_font: int = 5
    xys: Tuple[List[float], List[float]] = from_coordinate_list_to_xylist(vers)
    xs: List[float] = xys[0]
    ys: List[float] = xys[1]
    axis_len = int(radius) + 2
    plt.plot(xs, ys, 'ro')
    plt.axis([-axis_len, axis_len, -axis_len, axis_len])
    plt.autoscale(enable=True)
    for i_x, i_y in zip(xs, ys):
        plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y), fontsize=coord_font)


def make_edges(edges: List[Tuple[Tuple[float, float], Tuple[float, float]]]):
    lc = mc.LineCollection(edges, linewidths=0.5)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)


def plot_vers(vers: List[Tuple[float, float]], name='myfigure'):
    make_vers(vers)
    plt.savefig(name+'.pdf')
    plt.cla()
    plt.clf()
    plt.close('all')

def plot_edges(edges: List[Tuple[Tuple[float, float], Tuple[float, float]]],
               name='myfigure'):
    make_edges(edges)
    plt.savefig(name+'.pdf')
    plt.cla()
    plt.clf()
    plt.close('all')


def plot_graph(edges: List[Tuple[Tuple[float, float], Tuple[float, float]]],
               vers: List[Tuple[float, float]], name='myfigure'):
    make_edges(edges)
    make_vers(vers)
    fig.set_size_inches(18000.5, 10000.5)
    plt.savefig(name+'.pdf')
    plt.cla()
    plt.clf()
    plt.close('all')


def from_coordinate_list_to_xylist(vers: List[Tuple[float, float]]) -> \
        Tuple[List[float], List[float]]:
    xs: List[float] = list(map(lambda ver: ver[0], vers))
    ys: List[float] = list(map(lambda ver: ver[1], vers))
    return xs, ys
