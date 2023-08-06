import os
from typing import Iterable, List

from pydantic import BaseModel


class ModuleInfo(BaseModel):
    module_name: str
    absolute_path: str


class ModulesLoader:
    def __init__(self, linted_folders: List[str]):
        self.linted_folders = linted_folders

    def itermodules(self) -> Iterable:
        for linted_folder in self.linted_folders:
            root_folder_absolute_path = os.path.abspath(linted_folder)
            parent_module_name = root_folder_absolute_path.rsplit("/", maxsplit=1)[1]
            root_folder_absolute_path_size = len(root_folder_absolute_path)

            for parent_folder, _, child_files in os.walk(root_folder_absolute_path):
                for filename in child_files:
                    absolute_path = os.path.join(parent_folder, filename)
                    if filename.endswith(".py"):
                        yield ModuleInfo(
                            absolute_path=absolute_path,
                            module_name=parent_module_name
                            + absolute_path[root_folder_absolute_path_size:-3].replace(
                                "/", "."
                            ),
                        )
