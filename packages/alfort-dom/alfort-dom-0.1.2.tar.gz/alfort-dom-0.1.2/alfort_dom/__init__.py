from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version(__name__)
except PackageNotFoundError:
    __version__: str = "unknown"

from . import event
from .app import AlfortDom
from .local_storage import LocalStorage
from .location import Location

local_storage = LocalStorage()
location = Location()

__all__ = ["AlfortDom", "local_storage", "location", "event"]
