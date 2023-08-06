import csv
from Supplychain.Generic.folder_io import FolderWriter

from typing import Union


class CSVWriter(FolderWriter):

    def write_from_list(self, dict_list: list, file_name: str, ordering_key: Union[str, None] = None):
        with open(f"{self.output_folder}/{file_name}.csv", "w") as target_file:
            if dict_list:
                fieldnames = list(dict_list[0].keys())
                fieldnames.extend(
                    set(fieldname for row in dict_list for fieldname in row)
                    - set(fieldnames)
                )
                writer = csv.DictWriter(target_file, fieldnames=fieldnames, restval=None)
                writer.writeheader()
                to_be_writen = dict_list
                if ordering_key is not None and ordering_key in dict_list[0]:
                    to_be_writen = sorted(dict_list, key=lambda e: e[ordering_key])
                for row in to_be_writen:
                    to_be = {k: FolderWriter.json_value(v)
                             for k, v
                             in row.items()}
                    writer.writerow(to_be)

    def __init__(self,
                 output_folder: str = "Output"):
        FolderWriter.__init__(self,
                              output_folder=output_folder)
