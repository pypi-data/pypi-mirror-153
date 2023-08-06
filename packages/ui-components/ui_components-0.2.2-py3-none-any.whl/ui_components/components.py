from abc import ABC
from dataclasses import dataclass, fields
from datetime import date, datetime
from inspect import isclass
from itertools import count
from typing import Any, Dict, List, Optional, Union

from dominate import tags as d
from pydantic import Field
from pydantic.fields import UndefinedType


class component(d.html_tag, ABC):
    _counter = count()

    def __init__(
        self,
        component_tag: str,
        *args,
        **kwargs,
    ):

        # use the main element with no wrapper HTML.
        self.tagname = component_tag
        super().__init__(*args, **kwargs)
        self.element = self

    @property
    def seq_next(self) -> str:
        return str(next(self._counter))

    @property
    def width(self) -> float:
        return 0

    @property
    def height(self) -> float:
        return 0


class annotation(component):
    def __init__(
        self,
        label_text: Optional[str] = None,
        label_location: Union["left", "top", "top-center"] = "left",
        label_color: str = "green",
        tooltip_text: Optional[str] = None,
    ):
        if not label_text and not tooltip_text:
            raise ValueError("Either label_text or tooltip_text must be provided.")
        super().__init__("div")
        class_names = []
        if tooltip_text:
            class_names.append("tooltip")
            self.add(d.span(tooltip_text, _class="tooltiptext"))
        if label_text:
            if loc_cls := {
                "top-center": "centered-top-label",
                "top": "top-label",
            }.get(label_location):
                class_names.append(loc_cls)
            if label_location == "left" and not label_text.strip().endswith(":"):
                label_text = f"{label_text}: "
            if not hasattr(self.element, "id"):
                self.element.set_attribute("id", self.seq_next)
            self.add(d.label(label_text, _for=self.element.id))
            if label_location in ("top", "top-center"):
                self.add(d.br())
        # add the main element to it's wrapper HTML.
        # self.add(self.element)
        self.set_attribute("class", " ".join(class_names))


class select_options(component):
    """Generate a select element with options."""

    def __init__(
        self,
        options: List[str],
        optional: bool = False,
        default: Optional[str] = None,
        **kwargs,
    ):
        super().__init__("select", data_component="select_options", **kwargs)
        with self.element:
            if optional:
                d.option("-", value="-")
            for v in options:
                ele = d.option(v, value=v)
                if v == default:
                    ele.set_attribute("selected", "selected")


class multiselect(component):
    def __init__(
        self,
        options: List[str],
        allow_user_added: bool = False,
        **kwargs,
    ):
        super().__init__(
            "div",
            data_component="multiselect",
            _class="multiselect-container",
            **kwargs,
        )
        with self.element:
            with d.div(
                id="multiselect-selections-div", _class="multiselect-selections"
            ):
                for v in options:
                    d.span(
                        v,
                        _class="multiselect-option",
                        onclick="this.classList.toggle('multiselect-highlighted')",
                    )
            if allow_user_added:
                with d.span():
                    d._input(type="text", id="multiselect-user-option")
                    d.button(
                        "Add Option",
                        onmousedown="add_multiselect_option('multiselect-selections-div')",
                    )


class text_input(component):
    def __init__(
        self,
        optional: bool = True,
        suggestions: List[str] = [],
        **kwargs,
    ):
        if suggestions:
            super().__init__("span", data_component="text_input", **kwargs)
            list_id = kwargs.get("id") or self.seq_next
            with self.element:
                with d.datalist(id=list_id):
                    for s in suggestions:
                        d.option(s, value=s)
                with d._input(type="text", list=list_id, **kwargs) as ele:
                    if not optional:
                        ele.set_attribute("required", "required")
        else:
            super().__init__("input", **kwargs)
            if not optional:
                self.set_attribute("required", "required")


class option(select_options, component):
    """Generate an element to represent a boolean value. (a select element will be used if value is optional, else a checkbox)"""

    def __init__(
        self,
        optional: bool = False,
        default: Optional[bool] = None,
        **kwargs,
    ):
        if optional:
            select_options.__init__(
                self,
                options=["yes", "no"],
                optional=True,
                default={True: "yes", False: "no"}.get(default),
                **kwargs,
            )
        else:
            # If only two options, use a checkbox.
            component.__init__(self, "input", type="checkbox", **kwargs)
            if default == True:
                self.set_attribute("checked", "checked")
        self.set_attribute("data-component", "option")


class date_constraint(component):
    """Generate a datetime picker with a select element for conditional operators."""

    def __init__(
        self,
        conditions: List[str] = ["≺", "≤", "≻", "≥"],
        constraint_kwargs={},
        date_kwargs={},
    ):
        super().__init__("span", data_component="date_constraint")
        with self.element:
            select_options(
                optional=False,
                options=conditions,
                **constraint_kwargs,
            )
            d._input(type="datetime-local", **date_kwargs)


class kv_row(component):
    def __init__(
        self,
        header: List[str],
        title: str,
        data: Dict[str, Any],
        font_size_em: float = 1,
    ):
        self.font_size_em = font_size_em
        kwargs = (
            # TODO need units?
            {"style": f"font-size: {self.font_size_em};"}
            if self.font_size_em
            else {}
        )

        super().__init__("table", _class="kvt", **kwargs)
        with self.element:
            with d.caption(self.title, cls="kvt-title"):
                for key, value in self.rows[:-1]:
                    with d.tr(cls="inner"):
                        d.td(key, cls="key")
                        d.td(value, cls="value")
                key, value = self.rows[-1]
                with d.tr(cls="inner"):
                    d.td(key, cls="key")
                    d.td(value, cls="value")

    @property
    def width(self) -> float:
        # get max number of characters in row.
        longest_row = max(sum(len(cell) for cell in row) for row in self.rows)
        # 2 cols w/ l,r padding 1em
        total_padding_em = 4 * self.font_size_em
        total_text_em = longest_row * self.font_size_em * self.font_wh_ratio
        return total_padding_em + total_text_em

    @property
    def height(self) -> float:
        row_padding_em = 2
        total_padding_em = 3 * len(self.rows)
        total_text_em = len(self.rows) * self.font_size_em
        return total_padding_em + total_text_em


class kv_column(component):
    def __init__(self, header: List[str], title: str, font_size_em: float = 1):

        self.header = header
        self.font_wh_ratio = 0.7

        kwargs = (
            {"style": f"font-size: {self.font_size_em};"} if self.font_size_em else {}
        )

        super().__init__("table", _class="kvt")

        with self.element:
            d.caption(self.title, cls="kvt-title")
            with d.tr():
                for key, value in zip(self.header, self.row):
                    d.td(key, cls="key")
                    d.td(value, cls="value")

    @property
    def width(self) -> float:
        padding = 2 * len(self.header)
        text_width = sum(len(cell) for cell in self.row) * self.font_size_em
        return padding + text_width

    @property
    def height(self) -> int:
        return 3


def get_user_input_component(field: Field, instance_t: Optional[Any] = None):
    if instance_t is not None:
        default = getattr(instance_t, field.name)
        optional = False
    else:
        default = (
            None
            if isinstance(field.default.default, UndefinedType)
            else field.default.default
        )
        optional = (
            field.default.default is None
            or type(None) in field.type.__annotations__[field.name].__args__
        )
    if field.type in (str, float, int):
        suggestions = field.default.extra.get("suggestions", [])
        ele = text_input(optional, suggestions)
    elif field.type is bool:
        ele = option(optional, default)
    elif field.type in (datetime, date):
        # TODO select date default.
        ele = date_constraint()
    elif isinstance(field.type, list):
        ele = select_options(
            options=field.default.extra.get("choices") or default,
            default=default,
            optional=default is None,
        )
    else:
        raise ValueError("Unknown type")
    # add left label to element.
    return label(ele, field.name.title(), field.default.description)


class io_info_box(component):
    def __init__(
        self,
        DataClassT: Any,
        user_input: List[Any],
        metadata: List[Any],
        result: List[Any],
        children: List[Any],
    ):
        self.user_input = [label(to_component(f), f.name) for f in user_input]
        # if not provided with an instance, only display user input.
        if (is_instance := not isclass(DataClassT)) and metadata:
            pass
        if is_instance and result:
            pass

    @classmethod
    def from_dataclass(cls, DataClassT: Any):
        _fields = fields(DataClassT)
        sections = {
            tag: [f for f in _fields if tag in f.default.extra.get("tags")]
            for tag in ("user_input", "metadata", "result")
        }
        children = [
            cls.from_dataclass(f)
            for f in _fields
            if hasattr(f.type, "__dataclass_fields__")
        ]
        return cls(**sections, children=children)
