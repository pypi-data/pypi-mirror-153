import os
import json
from typing import Union


class FolderWriter:

    @staticmethod
    def json_value(element):
        """
        Dump an element as json for types with a different representation between json and python
        bool : no upper case starting letter
        list : can contain other elements so need to be dumped
        dict : python repr use simple quotes (') instead of double (") as used in json
        :param element: element to be converted
        :return: converted value of the element
        """
        if type(element) in (bool, dict, list):
            return json.dumps(element)
        return element

    def write_from_list(self, dict_list: list, file_name: str, ordering_key: Union[str, None] = None):
        pass

    def __init__(self,
                 output_folder: Union[str, None] = None):

        self.output_folder = output_folder
        if self.output_folder is not None:
            os.makedirs(self.output_folder, exist_ok=True)


class FolderReader:

    def __init__(self,
                 input_folder: str = "Output",
                 keep_nones: bool = True):
        self.input_folder = input_folder

        self.keep_nones = keep_nones

        self.files = None
