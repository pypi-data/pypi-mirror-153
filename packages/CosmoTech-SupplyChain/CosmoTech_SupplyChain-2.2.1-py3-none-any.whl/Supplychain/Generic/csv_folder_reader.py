import csv
import glob
import io
import json
import os

from collections import defaultdict

from Supplychain.Generic.folder_io import FolderReader


class CSVReader(FolderReader):
    extension = ".csv"

    def refresh(self):
        filenames = glob.glob(os.path.join(self.input_folder, "*" + self.extension))
        self.files = defaultdict(list)

        for filename in filenames:
            with open(filename, "r") as file:
                # Read every file in the input folder
                current_filename = os.path.basename(filename)[:-len(self.extension)]
                for row in csv.DictReader(file):
                    new_row = dict()
                    for key, value in row.items():
                        try:
                            # Try to convert any json row to dict object
                            converted_value = json.load(io.StringIO(value))
                        except json.decoder.JSONDecodeError:
                            converted_value = value
                        if converted_value == '':
                            converted_value = None
                        if converted_value is not None or self.keep_nones:
                            new_row[key] = converted_value
                    self.files[current_filename].append(new_row)

    def __init__(self,
                 input_folder: str = "Input",
                 keep_nones: bool = True):

        FolderReader.__init__(self,
                              input_folder=input_folder,
                              keep_nones=keep_nones)

        self.refresh()
