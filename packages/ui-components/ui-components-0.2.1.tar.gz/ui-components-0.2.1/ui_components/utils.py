import json
import operator
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, List, Optional

from dominate import tags as d
from dominate.document import document as document_t
from pydantic.dataclasses import dataclass
from ready_logger import logger

js_dir = Path(__file__).parent.joinpath("static", "js")
css_dir = Path(__file__).parent.joinpath("static", "styles")


def add_header(
    doc: document_t,
    js_files: List[str] = ["misc"],
    css_files: List[str] = ["common"],
    global_vars: Optional[Dict[str, Any]] = None,
) -> None:
    if global_vars:
        global_vars = {
            k: f"'{v}'" if isinstance(v, str) else v for k, v in global_vars.items()
        }
        for k, v in global_vars.items():
            doc.head.add_raw_string(f"<script>var {k}={v};</script>")
    for file in js_files:
        if not file.endswith(".js"):
            file += ".js"
        # d.script(js_dir.joinpath(file).read_text())
        # TODO fix script tag.
        doc.head.add_raw_string(
            f"""
            <script>
                {js_dir.joinpath(file).read_text()}
            </script>
            """
        )

    for file in css_files:
        if not file.endswith(".css"):
            file += ".css"
        # d.style(css_dir.joinpath(file).read_text())
        doc.head.add_raw_string(
            f"""
            <style>
                {css_dir.joinpath(file).read_text()}
            </style>
            """
        )

    with doc.head:
        # fonts.
        d.link(rel="preconnect", href="https://fonts.googleapis.com")
        d.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="")
        d.link(
            rel="stylesheet",
            type="text/css",
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap",
        )


def execute_query(engine, query: Any) -> bool:
    try:
        with engine.begin() as conn:
            conn.execute(query)
    except Exception as e:
        logger.error(f"Error executing query {query}: {e}")
        return e


def load_json(data: str) -> Any:
    try:
        return json.loads(data)
    except JSONDecodeError:
        logger.info("Invalid JSON syntax. Can not load.")


def request_field(field, req):
    if req.json:
        val = req.json.get(field)
    elif req.form:
        val = req.form.get(field)
    else:
        raise ValueError(
            "Request does not have JSON of form data. Can not extract field."
        )
    if val not in ("-", ""):
        return val


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
