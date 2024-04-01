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
        pass
