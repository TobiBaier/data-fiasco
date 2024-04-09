from utility.dataloader import DataLoader
from utility.filemanager import FileManager
from utility.diagrammaker import DiagramMaker

import os, re, json
import numpy as np
import matplotlib.pyplot as plt


class Control:
    draw: DiagramMaker
    file: FileManager
    data: DataLoader

    def __init__(self, draw: DiagramMaker, file: FileManager, data: DataLoader):
        self.data = data
        self.file = file
        self.draw = draw

        # standard settings
        self.mp_settings = None
        self.tx_settings = None
        self.ap_settings = None

        # load settings
        self.config()

    def config(self):
        with open("setup/standards/control_standards.json", "r") as of:
            settings = json.load(of)

        self.mp_settings = settings["multi_plot"]
        self.tx_settings = settings["twin_xscale"]
        self.ap_settings = settings["auto_plot"]

    def title_constructor(self, filename):
        return "a", "b"

    def auto_plot_data(self, filename, auto_title=True, **kwargs):

        tmp = filename
        filename = self.file.check_filename_format(filename)
        if not filename:
            print(f"not plotting: {tmp}")
            return None

        if "plot_kwargs" not in kwargs:
            kwargs["plot_kwargs"] = {}
        if "general" not in kwargs:
            kwargs["general"] = {}
        if "plt" not in kwargs:
            kwargs["plt"] = {}

        if "color" in kwargs:
            kwargs["plot_kwargs"]["color"] = kwargs.pop("color")
        if "ax" in kwargs:
            kwargs["general"]["ax"] = kwargs.pop("ax")
        if "title" in kwargs:
            kwargs["plt"]["title"] = kwargs.pop("title")
        if "suptitle" in kwargs:
            kwargs["plt"]["suptitle"] = kwargs.pop("suptitle")
        if "label" in kwargs:
            kwargs["plot_kwargs"]["label"] = kwargs.pop("label")
        if "draw" in kwargs:
            kwargs["general"]["draw"] = kwargs.pop("draw")
        if "save" in kwargs:
            kwargs["general"]["save"] = kwargs.pop("save")
        if "path" in kwargs:
            kwargs["general"]["path"] = kwargs.pop("path")
        else:
            kwargs["general"]["path"] = self.file.get_save_path(filename)

        ids = self.file.get_identifiers(filename)
        preset = None
        for i in ids:
            if i in self.draw.presets:
                preset = i
                break

        if "title" not in kwargs["plt"] and "suptitle" not in kwargs["plt"]:
            kwargs["plt"]["title"], kwargs["plt"]["suptitle"] = self.title_constructor(filename)

        rec_data = self.data.auto_read(self.file.get_data_path(filename))
        return self.draw.make_diagram(preset, rec_data, **kwargs)

    def create_combiplot(self, names):
        pass


def get_inst(path="C:/Users/baier/OneDrive/Programmierprojekte/data_fiasco"):
    di = DiagramMaker()
    fi = FileManager(path)
    da = DataLoader(fi)

    return Control(di, fi, da)


c = get_inst(path="C:/Users/baier/OneDrive/Programmierprojekte/data_fiasco")
c.auto_plot_data("sev_sebis110_bng2s096_na22_530_15min_hist_good.txt")

"""
C:/Users/baier/OneDrive/Programmierprojekte/data_fiasco
"""