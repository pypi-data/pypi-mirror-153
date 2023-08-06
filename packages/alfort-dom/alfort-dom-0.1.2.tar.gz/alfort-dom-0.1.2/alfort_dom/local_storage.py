from collections.abc import MutableMapping
from typing import Iterator

from js import localStorage  # type: ignore

_ignore_keys = ["0_commands", "0_interpreters"]


class LocalStorage(MutableMapping[str, str]):
    def __init__(self) -> None:
        self._storage = localStorage

    def __getitem__(self, key: str) -> str:
        item = self._storage.getItem(key)
        if item is None:
            raise KeyError(key)
        return item

    def __setitem__(self, key: str, value: str) -> None:
        self._storage.setItem(key, value)

    def __delitem__(self, key: str) -> None:
        self._storage.removeItem(key)

    def __len__(self) -> int:
        return self._storage.length

    def __iter__(self) -> Iterator[str]:
        return iter(k for k in self._storage.object_keys() if k not in _ignore_keys)
