import json
from Supplychain.Generic.folder_io import FolderWriter
from typing import Union


class JSONWriter(FolderWriter):

    def write_from_list(self, dict_list: list, file_name: str, ordering_key: Union[str, None] = None):
        with open(f"{self.output_folder}/{file_name}.json", "w") as target_file:
            if dict_list:
                to_be_writen = dict_list
                if ordering_key is not None and ordering_key in dict_list[0]:
                    to_be_writen = sorted(dict_list, key=lambda e: e[ordering_key])
                json.dump(list(to_be_writen), target_file, default=str)

    def __init__(self,
                 output_folder: str = "Output"):
        FolderWriter.__init__(self,
                              output_folder=output_folder)
