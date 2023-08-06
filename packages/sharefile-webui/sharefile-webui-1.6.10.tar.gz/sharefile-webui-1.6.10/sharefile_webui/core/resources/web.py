import os
from flask import Flask, Response, request, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from ..datafiles.file_tokens import FileTokens
from ..config import Config


templates_path = os.path.join(os.path.dirname(__file__), "../../templates/")
static_path = os.path.join(os.path.dirname(__file__), "../../static/")

app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
app_auth = HTTPBasicAuth()


def run_web(host: str, port: int):
    from .api.dir import Dir, DirRoot
    from .api.disk import Disk
    from .api.file import File
    from .api.file_content import FileContent
    from .api.file_token import FileToken
    from .api.file_upload import MultiFileUpload, MultiFileUploadRoot, SimpleFileUpload, SimpleFileUploadRoot

    with app.app_context():
        api = Api(app)
        api.add_resource(Dir, Dir.RESOURCE_URL)
        api.add_resource(DirRoot, DirRoot.RESOURCE_URL)
        api.add_resource(Disk, Disk.RESOURCE_URL)
        api.add_resource(File, File.RESOURCE_URL)
        api.add_resource(FileContent, FileContent.RESOURCE_URL)
        api.add_resource(FileToken, FileToken.RESOURCE_URL)
        api.add_resource(MultiFileUpload, MultiFileUpload.RESOURCE_URL)
        api.add_resource(MultiFileUploadRoot, MultiFileUploadRoot.RESOURCE_URL)
        api.add_resource(SimpleFileUpload, *SimpleFileUpload.RESOURCE_URL)
        api.add_resource(SimpleFileUploadRoot, *SimpleFileUploadRoot.RESOURCE_URL)
        app.run(host=host, port=port)


@app_auth.verify_password
def verify_password(username, password):
    users = Config.USERS
    return users.check_user(username, password)


@app.route("/", methods=["GET"])
@app_auth.login_required
def index() -> Flask.response_class:
    data = {
        "version": Config.VERSION,
        "user": app_auth.current_user()
    }
    return render_template("index.html", data=data)


@app.route("/share/<path:path>", methods=["GET"])
def share(path) -> Flask.response_class:
    args = request.args
    token = args.get("token", None)
    file_tokens: FileTokens = Config.FILE_TOKENS
    if path not in file_tokens.data:
        return f"File '{path}' not found", 404
    if file_tokens.check_token(path, token):
        full_path = os.path.join(Config.SHARE_DIRECTORY, path)
        if os.path.exists(full_path):
            return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))
        else:
            return f"404 File '{path}' not found.", 404
    return f"401 Unauthorized access to file '{path}'", 401


@app.route("/sharedir/<path:path>", methods=["GET"])
def sharedir(path) -> Flask.response_class:
    data = {}
    return render_template("index.html", data=data)


@app.route("/svgfilter/<path:path>", methods=["GET"])
def svg_filter(path) -> Flask.response_class:
    args = request.args
    find: str = args.get("find", None)
    replace: str = args.get("replace", None)
    full_path: str = os.path.join(static_path, path)
    content: str = None
    if os.path.splitext(path)[-1].lower() != ".svg":
        return f"406 Not Acceptable file extension in path '{path}'", 406
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            content = f.read()
        if find and replace:
            content = content.replace(find, replace)
    else:
        return f"404 File '{path}' not found.", 404

    return Response(content, mimetype="image/svg+xml")
