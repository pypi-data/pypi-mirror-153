import glob
import json
import os

from collections import defaultdict

from Supplychain.Generic.folder_io import FolderReader


class JSONReader(FolderReader):
    extension = ".json"

    def refresh(self):
        filenames = glob.glob(os.path.join(self.input_folder, "*" + self.extension))
        self.files = defaultdict(list)

        for filename in filenames:
            with open(filename, "r") as file:
                # Read every file in the input folder
                current_filename = os.path.basename(filename)[:-len(self.extension)]
                json_content = json.load(file)
                if type(json_content) is not list:
                    self.files[current_filename].append(json_content)
                else:
                    self.files[current_filename] = json_content
                if not self.keep_nones:
                    for i in self.files[current_filename]:
                        removed_keys = []
                        for k in i.keys():
                            if i[k] is None:
                                removed_keys.append(k)
                        for k in removed_keys:
                            del i[k]

    def __init__(self,
                 input_folder: str = "Input",
                 keep_nones: bool = True):

        FolderReader.__init__(self,
                              input_folder=input_folder,
                              keep_nones=keep_nones)

        self.refresh()
