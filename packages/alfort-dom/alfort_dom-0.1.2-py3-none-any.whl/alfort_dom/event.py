from typing import Any, Callable, Generic, TypeAlias, TypeVar

from alfort import Dispatch
from alfort.sub import Subscription, UnSubscription, subscription
from js import document  # type: ignore
from pyodide import create_proxy  # type: ignore

Msg = TypeVar("Msg")
Handler: TypeAlias = Callable[[Any], Msg]
Callback: TypeAlias = Callable[[Any], None]


class _Handler(Generic[Msg]):
    def __init__(self, fun: Any, key: Any):
        self.key = key
        self.fun = fun

    def __call__(self, *args: Any, **kwargs: Any) -> Msg:
        return self.fun(*args, **kwargs)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, _Handler):
            return False
        if isinstance(other, type(self.key)):
            return False
        return self.key == other.key


def handler(key: Any | None = None) -> Callable[[Handler[Msg]], _Handler[Msg]]:
    def _constructor(f: Handler[Msg]) -> _Handler[Msg]:
        _key = key if key is not None else tuple(f.__code__.co_lines())
        return _Handler[Msg](f, _key)

    return _constructor


_document_callbacks: dict[str, Callback] = {}


@create_proxy
def _document_listener(event: Any) -> None:
    if callback := _document_callbacks.get(event.type):
        callback(event)


def _create_subscriber(
    event_type: str,
) -> Callable[[Handler[Msg]], Subscription[Msg]]:
    def _subscriber(handler: Handler[Msg]) -> Subscription[Msg]:
        @subscription()
        def _subscription(dispatch: Dispatch[Msg]) -> UnSubscription:
            def _callback(e: Any) -> None:
                dispatch(handler(e))

            def _unsubscription() -> None:
                document.removeEventListener(event_type, _document_listener)
                del _document_callbacks[event_type]

            _document_callbacks[event_type] = _callback
            document.addEventListener(event_type, _document_listener)
            return _unsubscription

        return _subscription

    return _subscriber


on_keypress = _create_subscriber("keypress")
on_keydown = _create_subscriber("keydown")
on_keyup = _create_subscriber("keyup")

on_click = _create_subscriber("click")
on_mousemove = _create_subscriber("mousemove")
on_mousedown = _create_subscriber("mousedown")
on_mouseup = _create_subscriber("mouseup")
