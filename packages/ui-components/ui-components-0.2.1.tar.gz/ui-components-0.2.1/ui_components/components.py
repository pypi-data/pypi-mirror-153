from abc import ABC
from dataclasses import fields
from datetime import date, datetime
from inspect import isclass
from itertools import count
from typing import Any, List, Optional

from dominate import tags as d
from pydantic import Field
from pydantic.fields import UndefinedType


class component(d.html_tag, ABC):
    _id_seq = count()

    def __init__(self, outer_tag: str, *args, **kwargs):
        self.tagname = outer_tag
        super().__init__(*args, **kwargs)

    @property
    def next_id(self) -> str:
        return str(next(self._id_seq))


class select_options(component):
    """Generate a select element with options."""

    def __init__(
        self,
        options: List[str],
        optional: bool = False,
        default: Optional[str] = None,
        **kwargs,
    ):
        super().__init__("select", **kwargs)
        with self:
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
        # TODO change class name.
        super().__init__("div", _class="outer_select_container", **kwargs)
        with self:
            with d.div(id="selections", _class="selections_container"):
                for v in options:
                    d.span(
                        v,
                        _class="selection_option",
                        onclick="this.classList.toggle('highlighted_selection')",
                    )
            if allow_user_added:
                with d.span():
                    d._input(type="text", id="user_option")
                    d.button("Add Option", onmousedown="add_option('selections')")


class text_input(component):
    def __init__(
        self,
        optional: bool = True,
        suggestions: List[str] = [],
        **kwargs,
    ):
        if suggestions:
            super().__init__("span")
            _id = kwargs.get("id") or self.next_id
            list_id = f"{_id}_suggestions"
            with self:
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
                allow_none=True,
                default={True: "yes", False: "no"}.get(default),
                **kwargs,
            )
        else:
            # If only two options, use a checkbox.
            component.__init__(self, "input", type="checkbox", **kwargs)
            if default == True:
                self.set_attribute("checked", "checked")


class date_constraint(component):
    """Generate a datetime picker with a select element for conditional operators."""

    def __init__(
        self,
        conditions: List[str] = ["≺", "≤", "≻", "≥"],
        constraint_kwargs={},
        date_kwargs={},
    ):
        super().__init__("span")
        with self:
            select_options(
                allow_none=False,
                options=conditions,
                **constraint_kwargs,
            )
            d._input(type="datetime-local", **date_kwargs)


class label(component):
    """Add a left label and optional tooltip to an element."""

    def __init__(
        self,
        element: d.html_tag,
        label: Optional[str] = None,
        tooltip: Optional[str] = None,
    ):
        if not label and not tooltip:
            raise ValueError("Either `label` or `tooltip` must be provided.")
        if tooltip:
            super().__init__("span", class_name="tooltip")
            with self:
                d.span(tooltip, class_name="tooltiptext")
        else:
            super().__init__("span")
        if label:
            if not (label := label.strip()).endswith(":"):
                label = f"{label}: "
            if not hasattr(element, "id"):
                element.set_attribute("id", self.next_id)
            self += d.label(label, html_for=element.id)
        self += element


def get_user_input_component(field: Field, instance_t: Optional[Any] = None) -> label:
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
            allow_none=default is None,
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
