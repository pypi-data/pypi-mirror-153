import shutil
from .base import BaseResource
from ..web import app_auth


class Disk(BaseResource):
    RESOURCE_URL = "/api/disk/"

    @app_auth.login_required
    def get(self):
        usage = shutil.disk_usage(self.root_path)
        return {
            "status": True,
            "diskUsage": {
                "total": usage.total,
                "free": usage.free,
                "used": usage.used,
            }
        }
