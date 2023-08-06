import os
from argparse import Namespace
from .datafiles.users import Users
from .datafiles.file_tokens import FileTokens


class Config:
    VERSION = ""
    SHARE_DIRECTORY = ""
    USERS_DATAFILE_PATH = ""
    FILETOKENS_DATAFILE_PATH = ""
    USERS: Users = None
    FILE_TOKENS: FileTokens = None

    @classmethod
    def init(cls, app_args: Namespace, app_config_dir: str):
        cls.VERSION = app_args.version
        cls.SHARE_DIRECTORY = app_args.share_directory
        cls.USERS_DATAFILE_PATH = os.path.join(app_config_dir, "users.json")
        cls.FILETOKENS_DATAFILE_PATH = os.path.join(app_config_dir, "files.json")

        cls.USERS = Users(cls.USERS_DATAFILE_PATH)
        cls.FILE_TOKENS = FileTokens(cls.FILETOKENS_DATAFILE_PATH)
