import os
import json
import pandas as pd
import numpy as np


class DataLoader:

    def __init__(self):
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




