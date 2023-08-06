from CosmoTech_Acceleration_Library.Accelerators.adx_wrapper import ADXQueriesWrapper
from Supplychain.Generic.adx_wrapper import ADXWrapper
from Supplychain.Generic.folder_io import FolderWriter

from typing import Union


class ADXAndFileWriter():

    def write_target_file(self, dict_list: list, file_name: str, drop_by_tag: str = None):
        """
        Will wirte the data in the required format :
        - on disk if required, as csv files
        - on ADX if required
        :param dict_list: a list of dict objects to write
        :param file_name: the name of the file (without extension) which will be used as table name on ADX
        :return: None
        """
        if self.writer is not None:
            self.writer.write_from_list(dict_list=dict_list,
                                        file_name=file_name,
                                        ordering_key=None)
        if self.adx_connector:
            self.adx_connector.send_to_adx(dict_list, file_name, drop_by_tag=drop_by_tag)

    def __init__(self,
                 writer: Union[FolderWriter, None] = None,
                 adx_connector: Union[ADXQueriesWrapper, ADXWrapper, None] = None):
        """
        Init and execute transformation of the data
        :param reader: Folder reader serving files
        :param writer: Potential folder writer
        :param adx_connector: Potential connector to ADX
        """
        self.adx_connector = adx_connector

        self.writer = writer
