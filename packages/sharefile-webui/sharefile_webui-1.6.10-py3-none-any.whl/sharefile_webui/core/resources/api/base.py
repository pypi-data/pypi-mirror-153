import os
from flask_restful import Resource, reqparse, abort
from requests.utils import unquote
from ...config import Config


class BaseResource(Resource):
    class ArgumentLocation:
        ARGS = "args"
        FORM = "form"

    RESOURCE_URL = None

    def __init__(self):
        self.config: Config = Config
        self.root_path: str = self.config.SHARE_DIRECTORY
        self.parser: reqparse.RequestParser = reqparse.RequestParser()
        self.args: dict = None

    def _add_argument(self, name: str, type_: type = None, help_: str = None, location_: str = ArgumentLocation.ARGS):
        self.parser.add_argument(name, type=type_, help=help_, location=location_)
        self.args = self.parser.parse_args()

    def _check_path_perms(self, path: str) -> bool:
        rpath = os.path.realpath(path)
        return rpath.startswith(self.root_path)

    @staticmethod
    def _unquote_path(path):
        return unquote(path)

    @staticmethod
    def _get_file_ext(path):
        return os.path.splitext(path)[-1].lower().replace(".", "")

    @staticmethod
    def _check_and_create_dir(file_path: str):
        _dir, _file = os.path.split(file_path)
        if not os.path.exists(_dir):
            os.makedirs(_dir, exist_ok=True)

    @staticmethod
    def _abort_error(message: str):
        abort(400, message=message, status=False)
