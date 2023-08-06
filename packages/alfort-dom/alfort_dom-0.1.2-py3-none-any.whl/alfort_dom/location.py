from typing import Any

from js import location  # type: ignore


class _Getter:
    def __init__(self, key: str) -> None:
        self.key = key

    def __get__(self, _obj: Any, _objtype: Any = None) -> str:
        return str(getattr(location, self.key))


class _GetterAndSeter(_Getter):
    def __set__(self, _obj: Any, value: str) -> None:
        setattr(location, self.key, value)


class Location:
    __slots__ = []

    host = _Getter("host")
    hostname = _Getter("hostname")
    port = _Getter("port")
    pathname = _Getter("pathname")
    search = _Getter("search")
    search = _Getter("search")
    hash = _Getter("hash")
    origin = _Getter("origin")
    href = _GetterAndSeter("href")

    def assign(self, url: str) -> None:
        location.assign(url)

    def reload(self) -> None:
        location.reload()

    def replace(self, url: str) -> None:
        location.replace(url)

    def __str__(self) -> str:
        return self.href
