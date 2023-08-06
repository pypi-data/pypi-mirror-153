import os
import json
from types import SimpleNamespace
from pathlib import Path
from pprint import pformat

from Supplychain.Generic.timer import Timer

# prefix components:
space = '    '
branch = '│   '
# pointers:
tee = '├── '
last = '└── '


def tree(dir_path: Path, prefix: str = ''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


class CosmoAPIParameters(Timer):

    def __update(self):
        with open(os.path.join(self.folder_path, "parameters.json")) as f:
            self.parameters_file = json.load(f,
                                             object_hook=lambda d: SimpleNamespace(**d))

        self.parameters_folders = [dir_name for dir_name in os.listdir(self.folder_path)]
        self.datasets_folders = [dir_name for dir_name in os.listdir(self.dataset_folder_path)]

    def get_all_parameters(self):
        for p in self.parameters_file:
            yield p.parameterId, p.value

    def get_all_datasets_parameters(self):
        for p in self.parameters_file:
            if p.varType == "%DATASETID%":
                yield p.parameterId, self.get_dataset_path(p.parameterId)

    def get_dataset_path(self,
                         dataset_name: str) -> str:
        path = None
        try:
            path = self.get_named_parameter(dataset_name).value
        except ValueError:
            raise ValueError(f"Dataset {dataset_name} is not defined")

        if dataset_name not in self.parameters_folders and dataset_name not in self.datasets_folders:
            raise ValueError(f"Dataset ID {path} ({dataset_name}) was not downloaded")

        if dataset_name in self.parameters_folders:
            return os.path.join(self.folder_path, dataset_name)
        return os.path.join(self.dataset_folder_path, dataset_name)

    def get_named_parameter(self,
                            parameter_name: str) -> SimpleNamespace:
        for param in self.parameters_file:
            if parameter_name == param.parameterId:
                return param
        raise ValueError(f"Parameter {parameter_name} is not defined.")

    def update_parameter(self, parameter: dict):
        new_param = SimpleNamespace(**parameter)
        for param in self.parameters_file:
            if new_param.parameterId == param.parameterId:
                assert(new_param.varType == param.varType)
                param.value = new_param.value
                return
        self.parameters_file.append(new_param)

    def update_parameters(self, parameters: list):
        for parameter in parameters:
            self.update_parameter(parameter)

    def __init__(self,
                 parameter_folder: str,
                 dataset_folder: str):
        Timer.__init__(self, "[API Parameters]")
        self.folder_path = parameter_folder
        self.dataset_folder_path = dataset_folder

        self.parameters_file = None
        self.parameters_folders = None

        self.__update()

    def display_infos(self):

        self.display_message("Folders content")
        self.display_message(self.folder_path)
        for line in tree(Path(self.folder_path)):
            self.display_message(line)

        self.display_message(self.dataset_folder_path)
        for line in tree(Path(self.dataset_folder_path)):
            self.display_message(line)

        self.display_message("Parameters value")
        for _l in pformat(dict(self.get_all_parameters())).split('\n'):
            print(self.prefix, _l)

        self.display_message("Datasets parameters")
        for _l in pformat(dict(self.get_all_datasets_parameters())).split('\n'):
            print(self.prefix, _l)
