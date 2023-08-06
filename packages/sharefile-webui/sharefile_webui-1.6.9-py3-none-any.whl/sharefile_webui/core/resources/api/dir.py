import os
from datetime import datetime
from requests.utils import quote
from .base import BaseResource
from ..web import app_auth
from .file_content import FileContent


class Dir(BaseResource):
    RESOURCE_URL = "/api/dir/<path:path>"

    def __init__(self):
        super().__init__()
        self._add_argument("rename", str, "New filename for directory rename")

    @app_auth.login_required
    def get(self, path: str) -> dict:
        """
        List of directory files and subdirectories
        :param path: Direcotory to be listed
        """
        path = self._unquote_path(path)
        result_list_files = []
        result_list_dirs = []
        dir_path = os.path.join(self.root_path, path)
        if not os.path.exists(dir_path):
            self._abort_error(f"Directory '{dir_path}' does not exists.")

        try:
            dir_list: list = os.listdir(dir_path)
        except Exception as ex:
            self._abort_error(str(ex))

        dir_list.sort()

        if path:
            result_list_dirs.append({
                "type": "dir",
                "name": "/",
                "path": "",
            })
            result_list_dirs.append({
                "type": "dir",
                "name": "..",
                "path": os.path.sep.join(path.split(os.path.sep)[:-1]),
            })
        for dir_item in dir_list:
            full_path = os.path.join(dir_path, dir_item)
            context_item_path = os.path.join(path, dir_item)
            mdatetime = os.path.getmtime(full_path)
            if os.path.isfile(full_path):
                result_list_files.append({
                    "type": "file",
                    "name": dir_item,
                    "path": quote(context_item_path),
                    "size": os.path.getsize(full_path),
                    "mdatetime": mdatetime,
                    "mdatetimeISO": datetime.fromtimestamp(mdatetime).strftime("%Y-%m-%d %H:%M"),
                    "token": self.config.FILE_TOKENS.data.get(context_item_path, None),
                    "isEditable": FileContent.check_file_ext(full_path),
                })
            elif os.path.isdir(full_path):
                result_list_dirs.append({
                    "type": "dir",
                    "name": dir_item,
                    "path": quote(context_item_path),
                    "pathLabel": context_item_path,
                    "mdatetime": mdatetime,
                    "mdatetime-iso": datetime.fromtimestamp(mdatetime).strftime("%Y-%m-%d %H:%M"),
                })
        return {
            "status": True,
            "context": quote(path),
            "contextLabel": path,
            "result": result_list_dirs + result_list_files
        }

    @app_auth.login_required
    def delete(self, path: str) -> dict:
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        try:
            os.rmdir(full_path)
        except Exception as ex:
            self._abort_error(f"Dir.delete: {ex}")
        return {
            "status": True
        }

    @app_auth.login_required
    def post(self, path: str) -> dict:
        """
        Create new directory. If exists it will add number suffix
        :param path: New directory path
        """
        path = self._unquote_path(path)
        full_path: str = os.path.join(self.root_path, path)
        dir_tail: str = ""
        tail_counter: int = 1
        while os.path.exists(full_path_tail := f"{full_path}{dir_tail}"):
            dir_tail = f" {tail_counter}"
            tail_counter += 1
        os.mkdir(full_path_tail)
        return {
            "status": True,
            "dir": full_path_tail
        }

    @app_auth.login_required
    def put(self, path: str) -> dict:
        """
        Rename existing directory. New name comes in `rename` GET param
        :param path: Path to existing directory
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
                if self.config.FILE_TOKENS.remove_file_tokes_beginig(path):
                    self.config.FILE_TOKENS.save_json()
            except Exception as ex:
                self._abort_error(f"Dir.update: {ex}")
        return {
            "status": True,
            "dir": full_path_rename
        }


class DirRoot(Dir):
    RESOURCE_URL = "/api/dir/"

    @app_auth.login_required
    def get(self) -> dict:
        return super().get("")
