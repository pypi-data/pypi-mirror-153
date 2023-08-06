import json
import os


class BaseDatafile:
    def __init__(self, datafile_path: str):
        self._datafile_path: str = datafile_path
        self.data: dict = {}
        self.load_json()

    def load_json(self) -> bool:
        if os.path.exists(self._datafile_path):
            with open(self._datafile_path, "r") as f:
                self.data = json.load(f)
            return True
        return False

    def save_json(self):
        with open(self._datafile_path, "w") as f:
            json.dump(self.data, f)
