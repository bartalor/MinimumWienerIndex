import json
import os
import shutil
from pathlib import Path
from Conversions import networkx_to_coors, inp_vers_to_coors, networkx_to_outp_format
from Plot_Functions import plot_edges
from Tree_algorithm import print1, tree_algorithm
from planar import planar_algorithm

inp_dir_name = "inputs"
outp_dir_name = "outputs"
main_plots_dir_name = "output_plots"
Amir_ID = "311328314"
Bar_Id = "312577240"
mimshak_names = ["ld", "ya"]


def get_plots_dir_name(mim_name):
    return mim_name + "_plots"


def get_plots_dir_path(mim_name):
    return '/'.join([main_plots_dir_name, get_plots_dir_name(mim_name)])


def get_plot_path(mim_name, index, type):
    plots_dir_path = get_plots_dir_path(mim_name)
    assert os.path.exists(plots_dir_path)
    plot_name = '_'.join([mim_name, type, str(index)])
    return '/'.join([plots_dir_path, plot_name])


def get_inp_name(mim_name):
    return "Plane_" + mim_name + ".json"


def get_inp_path(mim_name):
    return "/".join([inp_dir_name, get_inp_name(mim_name)])


def get_outp_name(mim_name):
    return '_'.join([Amir_ID, Bar_Id, get_inp_name(mim_name)])


def get_outp_path(mim_name):
    return '/'.join([outp_dir_name, get_outp_name(mim_name)])


def fill_dict(inp_data, outp_dict, name):
    input_graphs = [inp_vers_to_coors(vers) for vers in inp_data["graphs"]]
    for i, vers in enumerate(input_graphs):
        print1("start working on graph number " +
               str(i) + " with " + str(len(vers)) + " vers!")
        plane_planar = planar_algorithm(vers)
        print1("finished planar graph " + str(i) + "!")
        plane_tree = tree_algorithm(vers)
        print1("finished tree graph " + str(i) + "!")
        plot_edges(networkx_to_coors(plane_planar, vers), get_plot_path(name, i, "planar"))
        plot_edges(networkx_to_coors(plane_tree, vers), get_plot_path(name, i, "tree"))
        outp_dict["graphs"].extend(
            [networkx_to_outp_format(plane_planar, i, "Planar"),
             networkx_to_outp_format(plane_tree, i, "Tree")])
        print1("finished writing graph " + str(i) + " to output dict!")


def work_on_files(name):
    outp_dict = {"graphs": []}
    with open(get_inp_path(name), 'r') as inp_f:
        inp_data = json.load(inp_f)
    fill_dict(inp_data, outp_dict, name)
    with open(get_outp_path(name), 'w+') as out_f:
        json.dump(outp_dict, out_f)


def create_folder(dir_path):
    os.mkdir(dir_path)
    assert os.path.exists(dir_path)


def create_folder_if_not_exist(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    assert os.path.exists(dir_path)


def delete_folder_if_exist(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    assert not os.path.exists(dir_path)


def main():
    assert os.path.exists(inp_dir_name)
    create_folder_if_not_exist(outp_dir_name)
    create_folder_if_not_exist(main_plots_dir_name)
    for name in mimshak_names:
        assert os.path.exists(get_inp_path(name))
        cur_plots_dir_path = get_plots_dir_path(name)
        if not os.path.exists(get_outp_path(name)):
            delete_folder_if_exist(cur_plots_dir_path)
            create_folder(cur_plots_dir_path)
            print1("start working on input file: " + get_inp_name(name))
            work_on_files(name)


main()
