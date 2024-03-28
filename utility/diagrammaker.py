import json
import os
import matplotlib.pyplot as plt
import locale
from pprint import pprint

locale.setlocale(locale.LC_ALL, "")

'''
DICTIONARY MERGE FUNCTION -------------------------------------------
'''


def merge(a: dict, b: dict, path=None):
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) or isinstance(b[key], list):
                if a[key] is None:
                    a[key] = b[key]
                elif b[key] is None:
                    a[key] = a[key]
            elif a[key] != b[key]:
                pass  # raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


"""
DIAGRAM MAKING ------------------------------------------------------
"""


def finish_diagram(params) -> None:
    if params["save"]:
        if params["path"] is None:
            plt.savefig("diagram.png", dpi=params["dpi"])
            print("Done Saving!")
        else:
            plt.savefig(params["path"], dpi=params["dpi"])
            print("Done Saving!")

    if params["draw"]:
        plt.show()


def stringify_command(key_list: list) -> str:
    if len(key_list) == 1:
        return str(key_list[0])

    else:
        key1 = str(key_list[0])
        key2 = str(key_list[1])

        if type(key_list[2]) is dict:
            settings = ""
            dict_settings = key_list[2]

            for key, entry in dict_settings.items():

                if type(entry) is str:
                    settings = settings + key + "=" + "'" + entry + "', "
                else:
                    settings = settings + key + "=" + f"{entry}" + ", "

            return f"{key1}.{key2}({settings})"

        else:
            if type(key_list[2]) is str:
                return f"{key1}.{key2}('{key_list[2]}')"
            else:
                return f"{key1}.{key2}({key_list[2]})"


def config_window(ax, params):
    for key1 in params:
        for key2, item in params[key1].items():
            cmd = stringify_command([key1, key2, item])

            try:
                eval(cmd)
            except (TypeError, NameError) as e:
                print(cmd + " raised " + e.__str__())

    return ax


def create_window(params):
    if params["ax"] is None:
        fig = plt.figure()
        return fig.add_subplot(111)
    else:
        return params["ax"]


'''
WRAPPERS FOR DIAGRAM CREATION ---------------------------------------
'''


def draw_plot(data, **kwargs):
    params = kwargs

    try:
        general_settings = params.pop("general")
    except KeyError:
        raise KeyError("There are no general settings provided (type=plot)!")

    try:
        plot_kwargs = params.pop("plot_kwargs")
    except KeyError:
        plot_kwargs = {}
        print("No plot_kwargs have been provided! Falling back to standard settings!")

    ax = create_window(general_settings)

    diagram = ax.plot(*data, **plot_kwargs)

    ax = config_window(ax, params)

    finish_diagram(general_settings)

    return diagram


def draw_hist(data, **kwargs):
    params = kwargs

    try:
        general_settings = params.pop("general")
    except KeyError:
        raise KeyError("There are no general settings provided (type=plot)!")

    try:
        plot_kwargs = params.pop("plot_kwargs")
    except KeyError:
        plot_kwargs = {}
        print("No plot_kwargs have been provided! Falling back to standard settings!")

    ax = create_window(general_settings)

    diagram = ax.stairs(*data, **plot_kwargs)

    ax = config_window(ax, params)

    finish_diagram(general_settings)

    return diagram


'''
ACTUAL DIAGRAM CLASS ------------------------------------------------
'''


class DiagramMaker:

    def __init__(self):
        self.standards = {}
        self.presets = {}
        self.load_setup()

    def load_setup(self):
        try:
            with open("../setup/presets/diagrammaker_presets.json", "rb") as of:
                self.presets = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load DiagramMaker-presets at "
                                    "'../setup/presets/diagrammaker_presets.json'!")

        try:
            with open("../setup/standards/diagrammaker_standards.json", "rb") as of:
                self.standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load DiagramMaker-standards at "
                                    "'../setup/standards/diagrammaker_standards.json'!")

    def make_diagram(self, preset, data, **kwargs):

        if preset not in self.presets:
            raise ValueError(f"{preset} is not a valid preset!")

        temp = self.presets[preset].copy()
        plot_type = temp.pop("plot_type")

        updated_presets = merge(kwargs, temp)

        if plot_type == "plot":
            return draw_plot(data, **merge(updated_presets, self.standards[plot_type]))

        elif plot_type == "hist":
            return draw_hist(data, **merge(updated_presets, self.standards[plot_type]))


if __name__ == "__main__":
    a = DiagramMaker()
    a.make_diagram("spec", [[1, 2, 3, 4, 5], [12, 45, 2, 3, 64]])
