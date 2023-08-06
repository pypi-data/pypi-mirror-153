#!/usr/bin/env python

"""
TODO: Allow public and private files
"""

import json
import sys
from pathlib import Path
from typing import Any, Optional


class Config:
    """
    Serialize a dictionary to json and read/write from config_file
    stored in ~/.config/<app_name>/<config_path>
    """

    def __init__(
        self,
        app_name: Optional[str] = None,
        _config_path: str = "config.json",
        **kwargs,
    ):
        """
        :param app_name: xxx
        :param _config_path: xxx
        :param kwargs: xxx
        """

        app_name = app_name or Path(sys.argv[0]).stem

        self.__dict__["_data"] = kwargs
        self.__dict__["_path"] = Path.home() / ".config" / app_name / _config_path

        if self._path.exists() and self._path.is_file():
            self._read()
        else:
            self._write()

    def __getattr__(self, name: str) -> Any:
        """
        :param name: xxx
        :returns: value assigned to Config for name
        """
        assert name in self._data, f"{name} not in config"
        return self._data[name]

    def __setattr__(self, name: str, value: Any) -> None:
        assert name in self._data, f"{name} not in config"
        self._data[name] = value
        self._write()

    def __delattr__(self, name: str) -> None:
        assert False, "Cannot delete from config"

    def _read(self) -> None:
        """Read config contents from json in config file"""
        with open(self._path) as json_file:
            data = json.load(json_file)

        # check to make sure keys are the same
        data_keys = set(data.keys())
        default_keys = set(self._data.keys())
        assert data_keys.issubset(
            default_keys
        ), f"{self._path} contains invalid keys: {(data_keys - default_keys)}"

        self.__dict__["_data"] = data

    def _write(self) -> None:
        """Write config contents to json in config file"""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as json_file:
            json.dump(self._data, json_file, sort_keys=True, indent=4)


if __name__ == "__main__":

    config = Config(_config_path="test.json", version=1, TOKEN="c5bffe0e")
    print(f"Value was {config.version}")
    config.version += 1
    print(f"Value is now {config.version}")
