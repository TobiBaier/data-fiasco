import os, re, json, shutil
from pprint import pprint



class FileManager:

    def __init__(self, root_path):

        # load root directory path
        self.path = root_path

        # load predefined directory paths
        self.data_path = self.path + "/data"
        self.condata_path = self.path + "/condensed_data"
        self.prodata_path = self.path + "/processed_data"
        self.graphs_path = self.path + "/graphs"
        self.sort_path = self.path + "/sortme"

        # catalogue path
        # self.cat_name = "sample_catalogue.json"

        # load setup, presets, sample catalogue
        self.presets = None
        # self.samples = None
        self.load_setup()

    def load_setup(self):

        # load sample catalogue
        # with open(self.path + self.cat_name, "r") as of:
        #     self.samples = json.load(of)

        # load presets
        with open("../setup/presets/filemanager_presets.json", "r") as of:
            self.presets = json.load(of)

        # extract given identifiers, if type is list or catalogue









a = FileManager("C:/Users/baier/OneDrive/Programmierprojekte/data_fiasco/")

pprint(a.presets)
