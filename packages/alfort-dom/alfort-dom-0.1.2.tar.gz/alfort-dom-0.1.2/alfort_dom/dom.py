import functools
from typing import Any, Callable, Protocol, TypeVar

from alfort import Dispatch, Effect
from js import document, window  # type: ignore
from pyodide import create_proxy  # type: ignore

M = TypeVar("M")


class HTMLElement(Protocol):
    def focus(self) -> None:
        ...

    @property
    def nodeValue(self) -> str:
        ...

    @nodeValue.setter
    def nodeValue(self, text: str) -> None:
        ...


def dom_effect(
    dom_id: str,
) -> Callable[[Callable[[HTMLElement, Dispatch[M]], None]], Effect[M]]:
    def _wrapper(fun: Callable[[HTMLElement, Dispatch[M]], None]) -> Effect[M]:
        @functools.wraps(fun)
        def _wrapped(dispatch: Dispatch[M]) -> None:
            def _f(_: Any) -> None:
                dom = document.getElementById(dom_id)
                fun(dom, dispatch)

            window.requestAnimationFrame(create_proxy(_f))

        return _wrapped

    return _wrapper
