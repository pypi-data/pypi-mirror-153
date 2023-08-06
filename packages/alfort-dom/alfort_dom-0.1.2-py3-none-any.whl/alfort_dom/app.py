from typing import Any, Callable, Generic, TypeVar

from alfort import Alfort, Dispatch, Enqueue, Init, Update, View
from alfort.sub import Subscriptions
from alfort.vdom import (
    Node,
    Patch,
    PatchInsertChild,
    PatchProps,
    PatchRemoveChild,
    PatchText,
    Props,
)
from js import HTMLElement, document, window  # type: ignore
from pyodide import JsProxy, create_proxy, to_js  # type: ignore

S = TypeVar("S")
M = TypeVar("M")


def _default_enqueue(render: Callable[[], None]) -> None:
    def _render(_: Any) -> None:
        render()

    window.requestAnimationFrame(create_proxy(_render))


class DomNode(Node, Generic[M]):
    dom: HTMLElement
    dispatch: Dispatch[M]
    handlers: dict[str, Callable[[Any], M]]
    listener: JsProxy

    def __init__(self, dom: HTMLElement, dispatch: Dispatch[M] | None = None) -> None:
        self.dom = dom
        self.dispatch = dispatch if dispatch is not None else lambda _: None
        self.handlers = {}

        def _listener(event: Any) -> None:
            if handler := self.handlers.get(event.type):
                self.dispatch(handler(event))

        self.listener = create_proxy(_listener)

    def apply(self, patch: Patch) -> None:
        match patch:
            case PatchInsertChild(child, None) if isinstance(child, DomNode):
                self.dom.insertBefore(child.dom, to_js(None))
            case PatchInsertChild(child, reference) if isinstance(
                child, DomNode
            ) and isinstance(reference, DomNode):
                self.dom.insertBefore(child.dom, reference.dom)
            case PatchRemoveChild(child) if isinstance(child, DomNode):
                self.dom.removeChild(child.dom)
            case PatchProps(remove_keys, add_props):
                if isinstance(add_props.get("style"), dict):
                    style = add_props.pop("style")
                    for k, v in style.items():
                        setattr(self.dom.style, k, v)

                for k in remove_keys:
                    if k.startswith("on"):
                        event_type = k[2:].lower()
                        self.dom.removeEventListener(event_type, self.listener)
                        del self.handlers[event_type]
                    else:
                        self.dom.removeAttribute(k)

                for k, v in add_props.items():
                    if k.startswith("on"):
                        event_type = k[2:].lower()
                        if v is not None:
                            if event_type in self.handlers:
                                self.dom.removeEventListener(event_type, self.listener)
                                del self.handlers[event_type]
                            if callable(v):
                                self.handlers[event_type] = v
                            else:
                                _v = v
                                self.handlers[event_type] = lambda _: _v
                            self.dom.addEventListener(event_type, self.listener)
                        else:
                            self.dom.removeEventListener(event_type, self.listener)
                            del self.handlers[event_type]
                    elif hasattr(self.dom, k):
                        setattr(self.dom, k, v)
                    else:
                        self.dom.setAttribute(k, v)
            case PatchText():
                self.dom.nodeValue = patch.value
            case _:
                raise ValueError(f"Unknown patch: {patch}")


class AlfortDom(Alfort[S, M, DomNode[M]]):
    def __init__(
        self,
        init: Init[S, M],
        view: View[S],
        update: Update[M, S],
        enqueue: Enqueue = _default_enqueue,
        subscriptions: Subscriptions[S, M] | None = None,
    ) -> None:
        super().__init__(init, view, update, enqueue, subscriptions)

    def create_text(
        self,
        text: str,
        dispatch: Dispatch[M],
    ) -> DomNode[M]:
        return DomNode(document.createTextNode(text), dispatch)

    def create_element(
        self,
        tag: str,
        props: Props,
        children: list[DomNode[M]],
        dispatch: Dispatch[M],
    ) -> DomNode[M]:
        dom_node = DomNode(document.createElement(tag, to_js({})), dispatch)

        for c in children:
            dom_node.apply(PatchInsertChild(c, None))

        dom_node.apply(PatchProps(remove_keys=[], add_props=props))
        return dom_node

    def main(
        self,
        root: str,
    ) -> None:
        self._main(DomNode[M](document.getElementById(root)))
