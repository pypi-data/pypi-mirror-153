from shopify_client.base_client import BaseClient
from .script_tag import ScriptTagCreate, ScriptTagUpdate, ScriptTagDelete


class ScriptTagClient(BaseClient):
    def create(self, request):
        return ScriptTagCreate().create(request)

    def update(self, request):
        return ScriptTagUpdate().update(request)

    def delete(self, request):
        return ScriptTagDelete().delete(request)
