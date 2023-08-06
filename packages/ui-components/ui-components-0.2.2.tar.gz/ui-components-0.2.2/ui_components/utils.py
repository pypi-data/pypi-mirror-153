import operator
from typing import Any

from pydantic.dataclasses import dataclass


def to_ascii_conditional_operator(operator_symbol: str):
    """Convert the weird symbols needed for HTML to regular ascii."""
    return {"≺": "<", "≤": "<=", "≻": ">", "≥": ">="}.get(
        operator_symbol, operator_symbol
    )


def condition(left: Any, operator_symbol: str, right: Any) -> bool:
    operator_symbol = to_ascii_conditional_operator(operator_symbol)
    operators = {
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
        ">=": operator.ge,
        ">": operator.gt,
    }
    if operator_symbol not in operators:
        raise ValueError(f"Unsupported operator: {operator_symbol}")
    return operators[operator_symbol](left, right)


@dataclass
class Point2d:
    x: int
    y: int


@dataclass
class BBox:
    top_: int = None
    left_: int = None
    bottom_: int = None
    right_: int = None
    width_: int = None
    height_: int = None

    def __post_init__(self):
        if not self.is_valid:
            raise ValueError("Not enough attributes provided to resolve properties.")
        self.update()

    def update(self, **kwargs):
        attrs = ("top", "left", "bottom", "right", "width", "height")
        if kwargs:
            # update attributes.
            for a in attrs:
                if a in kwargs:
                    setattr(self, f"{a}_", kwargs[a])
        # precompute dependant attributes.
        for a in attrs:
            setattr(self, f"{a}_", getattr(self, a))

    @property
    def is_valid(self) -> bool:
        """Return True if enough attributes are set for all the properties to resolve."""
        return (
            len([v for v in (self.top_, self.bottom_, self.height_)]) >= 2
            and len([v for v in (self.left_, self.right_, self.width_)]) >= 2
        )

    @property
    def top(self) -> int:
        return self.top_ or self.bottom - self.height

    @property
    def left(self) -> int:
        return self.left_ or self.right - self.width

    @property
    def right(self) -> int:
        return self.right_ or self.left + self.width

    @property
    def bottom(self) -> int:
        return self.bottom_ or self.top + self.height

    @property
    def width(self) -> int:
        return self.width_ or self.left - self.right

    @property
    def height(self) -> int:
        return self.height_ or self.bottom - self.top

    @property
    def x_center(self) -> int:
        return self.left + self.width / 2

    @property
    def y_center(self) -> int:
        return self.top + self.height / 2

    @property
    def top_center(self) -> Point2d:
        return Point2d(self.x_center, self.top)

    @property
    def bottom_center(self) -> Point2d:
        return Point2d(self.x_center, self.bottom)

    @property
    def left_center(self) -> Point2d:
        return Point2d(self.left, self.y_center)

    @property
    def right_center(self) -> Point2d:
        return Point2d(self.right, self.y_center)
