from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from lib.notion import Database
from notion_client import Client

if not settings.NOTION["integration_token"]:
    raise ImproperlyConfigured("NOTION_INTEGRATION_TOKEN is not set")

if not settings.NOTION["databases"]:
    raise ImproperlyConfigured("NOTION_DATABASES is not set")

for name, config in settings.NOTION["databases"].items():
    if not config["id"]:
        raise ImproperlyConfigured(f"NOTION_DATABASES.{name}.id is not set")

notion = Client(auth=settings.NOTION["integration_token"])

databases: dict[str, Database] = {}
for name, config in settings.NOTION["databases"].items():
    databases[name] = Database(notion, config["id"])

__all__ = ["notion", "databases"]
