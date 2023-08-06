import os
from .base import BaseResource
from ..web import app_auth


class File(BaseResource):
    RESOURCE_URL = "/api/file/<path:path>"

    def __init__(self):
        super().__init__()
        self._add_argument("rename", str, "New filename for directory rename")

    @app_auth.login_required
    def delete(self, path: str):
        path = self._unquote_path(path)
        if self.config.FILE_TOKENS.remove_file_token(path):
            self.config.FILE_TOKENS.save_json()
        full_path = os.path.join(self.root_path, path)
        os.remove(full_path)
        return {
            "status": True
        }

    @app_auth.login_required
    def put(self, path: str) -> dict:
        """
        Rename existing file. New name comes in `rename` GET param
        :param path: Path to existing file
        """
        path = self._unquote_path(path)
        rename = self.args.get("rename")
        if rename:
            path__1 = os.path.sep.join(path.split(os.path.sep)[:-1])
            full_path = os.path.join(self.root_path, path)
            full_path_rename = os.path.join(self.root_path, path__1, rename)
            if not self._check_path_perms(full_path_rename):
                self._abort_error(f"Permission denied to rename file '{full_path}' to '{full_path_rename}'")
            try:
                os.rename(full_path, full_path_rename)
                # delete all tokens under prevoius path name
                if self.config.FILE_TOKENS.remove_file_token(path):
                    self.config.FILE_TOKENS.save_json()
            except Exception as ex:
                self._abort_error(f"File.update: {ex}")
        return {
            "status": True,
            "file": full_path_rename
        }
