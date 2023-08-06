from __future__ import annotations

from .frame import Frame


class Scrollable:
    ...


class ScrollView(Frame):
    def __init__(self):
        Frame.__init__(self)


"""
from typing import Optional

from ._base import BaseWidget, TkWidget, ScrollableWidget
from .frame import Frame
from tukaan._tcl import Tcl


class ScrollView(BaseWidget, ScrollableWidget):
    _tcl_class = "ttk::frame"
    _keys = {
        "on_xscroll": ("func", "xscrollcommand"),
        "on_yscroll": ("func", "yscrollcommand"),
        "padding": tuple,
    }

    def __init__(
        self,
        parent: TkWidget | None,
        overflow: tuple[bool | str, bool | str] = ("auto", "auto"),
        padding: int | tuple[int, ...] | None = None,
    ):
        self._frame = BaseWidget(parent)
        

        Frame.__init__(self, parent=self._canvas, padding=padding)

    def _get(self, key: str):
        if key in {"on_xscroll", "on_yscroll"}:
            result = self._tcl_call(str, self._canvas, "cget", f"-{self._keys[key][1]}")
            return _callbacks[result]
        elif key == "padding":
            return convert_margin_back(self._tcl_call((int,), self, "cget", "-padding"))
        else:
            return BaseWidget._cget(self, key)

    def _set(self, **kwargs) -> None:
        on_xscroll = kwargs.pop("on_xscroll", None)
        on_yscroll = kwargs.pop("on_yscroll", None)
        padding = kwargs.pop("padding", None)
        if on_xscroll or on_yscroll:
            self._tcl_call(
                None,
                self._canvas,
                "config",
                *py_to_tcl_arguments(xscrollcommand=on_xscroll, yscrollcommand=on_yscroll),
            )
        if padding:
            kwargs["padding"] = convert_padding(padding)

        BaseWidget.config(self, **kwargs)

    def x_scroll(self, *args):
        self._tcl_call(None, self._canvas, "xview", *args)

    def y_scroll(self, *args):
        self._tcl_call(None, self._canvas, "yview", *args)

"""
