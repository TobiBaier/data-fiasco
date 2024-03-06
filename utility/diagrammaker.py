import json
import os
import matplotlib.pyplot as plt
import locale
from pprint import pprint

locale.setlocale(locale.LC_ALL, "")


class DiagramMaker:

    def __init__(self):
        self.standards = {}
        self.presets = {}
        self.load_setup()

    def load_setup(self):
        try:
            with open("../setup/presets/diagrammaker_presets.json", "r") as of:
                self.presets = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load DiagramMaker-presets at "
                                    "'../setup/presets/diagrammaker_presets.json'!")

        try:
            with open("../setup/standards/diagrammaker_standards.json", "r") as of:
                self.standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load DiagramMaker-standards at "
                                    "'../setup/standards/diagrammaker_standards.json'!")

    def make_diagram(self, preset, data, **kwargs):

        if preset not in self.presets:
            raise ValueError(f"{preset} is not a valid preset!")

        plot_type = self.presets[preset]["plot_type"]

        temp = self.presets[preset].copy()
        temp.pop("plot_type")
        for key in kwargs:
            if key in temp:

                for inner_key in kwargs[key]:
                    if type(kwargs[key][inner_key]) == dict and inner_key in temp[key]:
                        kwargs[key][inner_key] = temp

                if type(temp[key]) == dict and type(kwargs[key]) == dict:
                    for inner_key in kwargs[key]:
                        pass
                else:
                    print(f"{key} has to link to a dictionary type!")

                    kwargs[key] = temp[key] | kwargs[key]




def merge(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) or isinstance(b[key], list):
                if a[key] == None:
                    a[key] = b[key]
                elif b[key] == None:
                    a[key] = a[key]
            elif a[key] != b[key]:
                pass # raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a



# print([92, 32] + [None])


a = DiagramMaker()

b = merge(dict(a.presets["sev"]), a.standards["hist"])

c = {
    "ax":{
        "set_xlabel": "test"
    }
}

pprint(merge(c, b))




# eval(---) throws a NameError

