from typing import Union
from Supplychain.Generic.folder_io import FolderWriter, FolderReader


class MemoryFolderIO(FolderWriter, FolderReader):

    def reset(self):
        self.files = dict()

    def write_from_list(self, dict_list: list, file_name: str, ordering_key: Union[str, None] = None):
        if dict_list:
            to_be_writen = dict_list
            if ordering_key is not None and ordering_key in dict_list[0]:
                to_be_writen = sorted(dict_list, key=lambda e: e[ordering_key])
            self.files[file_name] = to_be_writen

    def __init__(self):

        FolderReader.__init__(self)
        FolderWriter.__init__(self)

        self.reset()
