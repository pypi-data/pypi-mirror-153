from Supplychain.Generic.folder_io import FolderWriter
from typing import Union

import os

from openpyxl import Workbook
from openpyxl.styles import Font


class ExcelWriter(FolderWriter):

    def write_from_list(self, dict_list: list, file_name: str, ordering_key: Union[str, None] = None):
        sheet = self.work_book.create_sheet(file_name)
        if dict_list:
            _keys = tuple(dict_list[0].keys())

            # write header :
            sheet.append(_keys)

            to_be_writen = dict_list
            if ordering_key is not None and ordering_key in _keys:
                to_be_writen = sorted(dict_list, key=lambda e: e[ordering_key])
            for row in to_be_writen:

                to_be = {k: FolderWriter.json_value(v)
                         for k, v
                         in row.items()}
                sheet.append(to_be.get(k, None) for k in _keys)

            bold_font = Font(bold=True)
            sheet.row_dimensions[1].font = bold_font

            dims = {}
            for row in sheet.rows:
                for cell in row:
                    if cell.value:
                        dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
            for col, value in dims.items():
                sheet.column_dimensions[col].width = value*1.1
        self.work_book.save(os.path.join(self.output_folder, self.target_file_name))

    def __init__(self,
                 output_folder: str = "Output"):
        FolderWriter.__init__(self,
                              output_folder=output_folder)

        self.target_file_name = "Dataset.xlsx"

        self.work_book = Workbook()
        del self.work_book['Sheet']
