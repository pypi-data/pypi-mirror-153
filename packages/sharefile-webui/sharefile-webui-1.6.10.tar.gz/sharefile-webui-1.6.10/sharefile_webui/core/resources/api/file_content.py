import markdown
import os
import re
from .base import BaseResource
from ..web import app_auth


class FileContent(BaseResource):
    class AllowedExtension:
        TXT = "txt"
        MD = "md"
        LOG = "log"

    RESOURCE_URL = "/api/filecontent/<path:path>"
    ALLOWED_EXTENSIONS = [AllowedExtension.TXT, AllowedExtension.MD, AllowedExtension.LOG]
    MAX_FILE_SIZE = 64 * 1024

    def __init__(self):
        super().__init__()
        self._add_argument("content", str, "File content to store", location_=self.ArgumentLocation.FORM)
        self._add_argument("decode-content", bool, "Decode content into HTML", location_=self.ArgumentLocation.ARGS)

    @app_auth.login_required
    def get(self, path):
        decode_content = self.args.get("decode-content")
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        if not self.check_file_ext(full_path):
            self._abort_error("Unsupported file extension to get file content")
        if (filesize := os.path.getsize(full_path)) > self.MAX_FILE_SIZE:
            self._abort_error(f"File size reached max size {filesize} > {self.MAX_FILE_SIZE} Bytes")
        with open(full_path, "r") as f:
            content = f.read()
        return {
            "status": True,
            "content": self._decode_content(self._get_file_ext(path), content) if decode_content else content,
            "name": os.path.basename(path),
            "path": path,
            "fullpath": full_path
        }

    @app_auth.login_required
    def post(self, path):
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        file_tail: str = ""
        tail_counter: int = 1
        while os.path.exists(full_path_tail := f"{full_path}{file_tail}.txt"):
            file_tail = f" {tail_counter}"
            tail_counter += 1
        os.mknod(full_path_tail)
        return {
            "status": True,
            "fullpath": full_path_tail
        }

    @app_auth.login_required
    def put(self, path):
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        if not self.check_file_ext(full_path):
            self._abort_error("Unsupported file extension to get file content")

        content = self.args.get("content")
        if content is not None:
            with open(full_path, "w") as f:
                f.write(content)
            return {
                "status": True,
                "file": full_path,
            }
        self._abort_error(f"Content of request for file '{path}' is empty.")

    @classmethod
    def check_file_ext(cls, path: str) -> bool:
        return cls._get_file_ext(path) in cls.ALLOWED_EXTENSIONS

    @classmethod
    def _decode_content(cls, file_extension: str, content: str) -> str:
        if file_extension in (cls.AllowedExtension.TXT, cls.AllowedExtension.LOG):
            # replace URLs in text by links
            url_list = re.findall(r'(https?://[^\s]+)', content)
            for url in url_list:
                content = content.replace(url, f"<a href=\"{url}\">{url}</a>")
            # replace new lines as BR tags
            content = content.replace("\n", "<br/>")
            return content
        elif file_extension == cls.AllowedExtension.MD:
            return markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        return content
