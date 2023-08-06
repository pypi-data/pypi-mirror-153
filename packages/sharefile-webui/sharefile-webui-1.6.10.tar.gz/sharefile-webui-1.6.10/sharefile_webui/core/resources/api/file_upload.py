import os
from flask_restful import request
from .base import BaseResource
from ..web import app_auth


class MultiFileUpload(BaseResource):
    RESOURCE_URL = "/api/multiupload/<path:path>"

    @app_auth.login_required
    def post(self, path: str):
        path = self._unquote_path(path)
        return self.post_chunk_upload(path)

    def post_chunk_upload(self, path: str):
        chunk_offset: int = int(request.form.get("dzchunkbyteoffset"))
        file: dict = request.files.get("file", {})
        file_path: str = os.path.join(self.root_path, path, file.filename)
        with open(file_path, 'ab') as f:
            f.seek(chunk_offset)
            chunk = file.stream.read()
            f.write(chunk)
        return {
            "status": True,
            "chunkSize": len(chunk),
            "chunkNumber": int(request.form.get("dzchunkindex")),
            "chunkTotalNumber": int(request.form.get("dztotalchunkcount")),
            "currentRemoteFileSize": os.path.getsize(file_path),
            "totalFileSize": int(request.form.get("dztotalfilesize")),
            "filename": file.filename,
            "remotePath": file_path
        }

    def post_multiupload(self, path: str):
        uploaded = []
        files = request.files
        for file_item in files.items():
            _, file_storage = file_item
            filename = file_storage.filename
            full_file_path = os.path.join(self.config.SHARE_DIRECTORY, path, filename)
            self._check_and_create_dir(full_file_path)
            file_storage.save(full_file_path)
            uploaded.append(filename)
        return {
            "status": True,
            "filename": uploaded,
            "fullpath": full_file_path
        }


class MultiFileUploadRoot(MultiFileUpload):
    RESOURCE_URL = "/api/multiupload/"

    @app_auth.login_required
    def post(self):
        return super().post("")


class SimpleFileUpload(BaseResource):
    """
    Example of CURL upload:
    curl -X POST -H "Content-Type: multipart/form-data" -u "admin:pass" -F "file=@FILENAME" "http://localhost:7777/api/upload/DIRECTORY"
    """
    RESOURCE_URL = ["/api/upload/<path:path>", "/api/uploadandshare/<path:path>"]

    @app_auth.login_required
    def post(self, path: str):
        ret = {
            "status": False
        }
        path = self._unquote_path(path)
        file_storage = request.files["file"]
        if file_storage.filename:
            file_path = os.path.join(path, file_storage.filename)
            full_file_path = os.path.join(self.config.SHARE_DIRECTORY, file_path)
            self._check_and_create_dir(full_file_path)
            file_storage.save(full_file_path)
            ret = {
                "status": True,
                "filename": file_path,
                "fullpath": full_file_path
            }
            if request.path.startswith("/api/uploadandshare/"):
                token = self.config.FILE_TOKENS.add_file_token(file_path)
                self.config.FILE_TOKENS.save_json()
                ret["token"] = token
                ret["sharelink"] = f"{request.host_url}share/{file_path}?token={token}"
        return ret


class SimpleFileUploadRoot(SimpleFileUpload):
    RESOURCE_URL = ["/api/upload/", "/api/uploadandshare/"]

    @app_auth.login_required
    def post(self):
        return super().post("")
