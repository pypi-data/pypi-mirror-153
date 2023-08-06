from dataclasses import dataclass, field
import os
from typing import List

from tlint.configuration import Configuration
from tlint.linters.forbidden_imports import ForbiddenImportsLinter
from tlint.linters.linter_interface import ILinter
from tlint.loader import ModuleInfo, ModulesLoader

@dataclass
class LinterChain:
    linters: List[ILinter] = field(default_factory=list)

    def add(self, linter: ILinter):
        self.linters.append(linter)

    def lint_module(self, module_info: ModuleInfo):
        for linter in self.linters:
            linter.lint_module(module_info)


class TLint:
    def __init__(self):
        self.__reload_config()

    def __reload_config(self):
        """Load or reload tlint config from a YAML file.

        If environment variable LINTIT_CONFIG is set, it is used as config file path.
        Otherwise config file is assumed to be located either at tlint.yaml or ~/tlint.yaml
        """
        config_file_path = os.getenv("LINTIT_CONFIG")
        if config_file_path is None:
            config_file_path = os.path.abspath("tlint.yaml")

        self.config = Configuration.from_file(config_file_path)

    def build_linter_from_config(self):
        root_linter = LinterChain()
        if len(self.config.protected_modules) > 0:
            root_linter.add(ForbiddenImportsLinter(self.config.protected_modules))
        return root_linter

    def lint(self):
        linter = self.build_linter_from_config()
        modules_loader = ModulesLoader(self.config.linted_folders)
        for moduleinfo in modules_loader.itermodules():
            linter.lint_module(moduleinfo)
