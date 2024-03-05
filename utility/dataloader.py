import os
import json
import pandas as pd
import numpy as np
from pprint import pprint

try:
    from filemanager import FileManager
except ModuleNotFoundError:
    print("ATTENTION! Operating without FileManager! Only read functions will work!")


class DataLoader:

    cfile: FileManager

    def __init__(self, cfile: FileManager):
        self.cfile = cfile

        self.standards = {}
        self.presets = {}
        self.load_setup()

    def load_setup(self):
        try:
            with open("../setup/presets/dataloader_presets.json", "r") as of:
                self.presets = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load Dataloader-presets at"
                                    "'../setup/presets/dataloader_presets.json'!")

        try:
            with open("../setup/standards/dataloader_standards.json", "r") as of:
                self.standards = json.load(of)
        except FileNotFoundError:
            raise FileNotFoundError("Could not load Dataloader-standards at"
                                    "'../setup/standards/dataloader_standards.json'!")

    def auto_read(self, path):

        current_settings = {}

        ending = path.split(".")[-1]
        if ending in self.standards:
            current_settings = self.standards[ending] | current_settings
        else:
            raise TypeError(f"The ending '{ending}' cannot be read!")



        ids, id_names = self.cfile.get_identifiers(path, return_id_names=True)

        for name, id in zip(id_names, ids):
            if name in self.presets:
                if id in self.presets[name]:
                    for key in current_settings:
                        if key in self.presets[name][id]:
                            current_settings[key] = self.presets[name][id][key] | current_settings[key]

        if "data_type" in current_settings["settings"]:
            if current_settings["settings"]["data_type"] != ending:
                print(f"The provided file type '.{ending}' does not match the expected file type "
                      f"'.{current_settings['data_type']}'! Trying to read anyway.")
            current_settings["settings"].pop("data_type")

        pprint(current_settings)

    def data_from_csv(self, filepath: str, **kwargs):

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"There is no file at {filepath}. Please remember to enter a full path!")

        if "data-format" in kwargs:
            read_params = kwargs["data-format"]
        else:
            read_params = {}

        # read data
        data = pd.read_csv(filepath, ** read_params)

        # define some vars for clarity
        swap_axes = False
        if "swap_axes" in kwargs["settings"]:
            swap_axes = kwargs["settings"]["swap_axes"]
        bin_ret = False
        if "bin_ret" in kwargs["settings"]:
            bin_ret = kwargs["settings"]["bin_ret"]

        if swap_axes:
            if not bin_ret:
                return data.to_numpy().swapaxes(0, 1)
            else:
                x, y = data.to_numpy().swapaxes(0, 1)
                bin_width = x[1] - x[0]
                x = x - 0.5 * bin_width
                return y, np.append(x, x[-1] + bin_width)
        else:
            return data.to_numpy

    def data_from_txt(self, filepath, **kwargs):

        return self.data_from_csv(filepath, **kwargs)








fi = FileManager("Z:\Studenten\Baier\sample-data")
dl = DataLoader(fi)

dl.auto_read("Z:\Studenten\Baier\sample-data\data\sev\sebis110\sev_sebis110_bng2s096_na22_530_15min_hist_good.txt")
