import os, re, json, shutil
from pprint import pprint
# import numpy as np


def test_identifier(text, identifier):
    # test for catalogue type
    if identifier["type"] == "from-catalogue":
        if text not in identifier["content"].keys():
            return False
        else:
            return text

    # test for list type
    if identifier["type"] == "from-list":
        if text not in identifier["content"]:
            return False
        else:
            return text

    # test for regex type
    if identifier["type"] == "regex":
        if re.search(identifier["content"], text) is None:
            return False
        else:
            if re.search(identifier["content"], text).group(0) == text:
                return text

    # if previous if-statements did not return, return False, as no identifier has been found
    return False


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

        # load presets, save identifiers extra
        self.identifiers = {}
        self.presets = None
        self.load_setup()

    def load_setup(self):

        # load sample catalogue
        # with open(self.path + self.cat_name, "r") as of:
        #     self.samples = json.load(of)

        # load presets
        with open("../setup/presets/filemanager_presets.json", "r") as of:
            self.presets = json.load(of)

        # extract given identifiers, if type is list or catalogue
        for i, identifier in enumerate(self.presets["identifiers"]):
            # construct basis dict, saving ident position, type and content
            self.identifiers[identifier] = {
                "type": self.presets["identifiers"][identifier]["type"],
                "position": i,
                "content": None,
                "sort-by": self.presets["identifiers"][identifier]["sort-by"],
            }

            # list is provided
            if self.identifiers[identifier]["type"] == "from-list":
                self.identifiers[identifier]["content"] = self.presets["identifiers"][identifier]["list"]

            # dict is extracted from a json file -> keys should be allowed identifiers
            elif self.identifiers[identifier]["type"] == "from-catalogue":
                with open(self.presets["identifiers"][identifier]["path"], "r") as of:
                    self.identifiers[identifier]["content"] = json.load(of)

            # regex string is saved
            elif self.identifiers[identifier]["type"] == "regex":
                self.identifiers[identifier]["content"] = self.presets["identifiers"][identifier]["r-string"]

    def check_filename_format(self, filename, check_identifier=True, check_rest=True):
        name_elements = filename.split("_")

        if check_identifier:
            if not self.check_identifiers(filename):
                return False

        if check_rest:
            for key, value in self.presets["filename criteria"].items():
                if key == "forbidden endings":
                    for ending in value:
                        if ending in filename:
                            print(f"Ending {ending} is not allowed!")
                            return False

                # for specific names, requirements can be defined
                elif key in filename:
                    # name must contain a certain phrase
                    if value["contains"]:
                        for text in value["contains"]:
                            if text not in filename:
                                print(f"{text} has to be in a filename of type {key}!")
                                return False

                    # name must end in a defined ending
                    if value["ending"]:
                        if "." in filename:
                            if value["ending"] not in filename:
                                print(f"A file for {key} has to end in {value['ending']}!")
                                return False
                        else:
                            return filename + value["ending"]

        return filename

    def check_identifiers(self, filename, sort_only=False):
        name_elements = filename.split("_")

        # this does a positional check as well (in comparison to test_identifier)
        for name, identifier in self.identifiers.items():

            if identifier["sort-by"] is False and sort_only is True:
                continue

            if identifier["type"] == "from-catalogue":
                if name_elements[identifier["position"]] not in identifier["content"].keys():
                    print(f"Name does not contain '{name}' identifier of type from-catalogue!")
                    return False

            if identifier["type"] == "from-list":
                if name_elements[identifier["position"]] not in identifier["content"]:
                    print(f"Name does not contain '{name}' identifier of type from-list!")
                    return False

            if identifier["type"] == "regex":
                if re.search(identifier["content"], name_elements[identifier["position"]]) is None:
                    print(f"Name does not contain '{name}' identifier of type regex!")
                    return False

        return True

    def get_identifiers(self, filename):
        check_ret = self.check_identifiers(filename)
        name_elements = filename.split("_")

        # if not all identifier are given, cycle through the name and check if any are in there
        if not check_ret:
            print("WARNING: Filename does not contain all defined identifiers!")
            for i, element in enumerate(name_elements.copy()):
                for identifier in self.identifiers.values():
                    if test_identifier(element, identifier) is False:
                        name_elements[i] = False
                    else:
                        name_elements[i] = element
                        break

            return [i for i in name_elements if i is not False]

        # if all identifiers are at the specified locations, return them
        else:
            return name_elements[0:len(self.identifiers)]

    def get_data_path(self, filename, check_identifier=True, check_rest=True):
        """

        :param check_identifier:
        :param check_rest:
        :param filename:
        :return:
        """

        path = self.data_path

        # retrieve a list of identifiers in name -> construct a filename from that
        ids = self.get_identifiers(filename)
        for i, identifier in enumerate(self.identifiers.values()):

            # only use ids, by which database is sorted
            if identifier["sort-by"] and ids != []:

                # if id is not included, skip iteration -> errors are handled later
                if ids[i] is None:
                    continue

                # add id to the path
                path = path + "/" + ids[i]

        # check, if file validates given constraints on filename format
        temp = self.check_filename_format(filename, check_identifier=check_identifier, check_rest=check_rest)

        # path may not link to a file if wrong ids were give -> do a full search for it
        if temp and os.path.isfile(path + "/" + temp):
            return path + "/" + temp
        else:
            return self.search_data_path(filename)

    def search_data_path(self, filename):
        for root, direc, files in os.walk(self.data_path):
            if filename in files:
                return os.path.join(root, filename)

        print("Tried to find any file with given name but failed. Check if ending is included.")

        return False

    def get_save_path(self, filename):

        try:
            return self.get_data_path(filename).replace(self.data_path, self.prodata_path)
        except AttributeError:
            return 



a = FileManager("C:/Users/baier/OneDrive/Programmierprojekte/data_fiasco/")
# print(a.get_identifiers("sev_bis105_bcg2s060_na22_hist_good.txt"))
print(a.get_save_path("ahh.test"))