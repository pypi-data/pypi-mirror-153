import os
from flask_restful import request
from .base import BaseResource
from ..web import app_auth


class FileUpload(BaseResource):
    RESOURCE_URL = "/api/upload/<path:path>"

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
            file_path = os.path.join(self.config.SHARE_DIRECTORY, path, filename)
            file_storage.save(file_path)
            uploaded.append(filename)
        return {
            "status": True,
            "filename": uploaded,
        }


class FileUploadRoot(FileUpload):
    RESOURCE_URL = "/api/upload/"

    @app_auth.login_required
    def post(self):
        return super().post("")
