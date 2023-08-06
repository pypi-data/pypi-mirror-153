from enum import Enum
from typing import List, Optional

import yaml
from pydantic import BaseModel, parse_obj_as


class ModuleAccessPolicy(Enum):
    GRANT = "grant"
    DENY = "deny"


class ModuleAccessConfiguration(BaseModel):
    pattern: str
    policy: ModuleAccessPolicy
    forbidden: Optional[List[str]]
    authorized: Optional[List[str]]


class Configuration(BaseModel):
    linted_folders: List[str]
    protected_modules: List[ModuleAccessConfiguration]

    @staticmethod
    def from_file(filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as config_file:
                config = yaml.safe_load(config_file)
        except FileNotFoundError:
            print(f"Config file not found in {filename}")
            exit(1)
        return parse_obj_as(Configuration, config)
