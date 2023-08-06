import re
from collections import defaultdict
from pathlib import Path
from textwrap import dedent
from typing import Any, Callable, Dict, List, Optional, Union

from dominate import document
from dominate import tags as d
from lxml.html import fromstring

from .styles import all_styles

js_dir = Path(__file__).parent.joinpath("js")
# js_dir = Path("/home/dan/my-github-packages/ui-components/ui_components/js")


def get_js_func_files():
    """Map function name to JS file."""
    js_func_files = []
    for f in js_dir.glob("*.js"):
        file_content = f.read_text()
        func_names = [
            m.group(1) for m in re.finditer(r"(?:^|\s|\n)function (\w+)", file_content)
        ]
        for func_name in func_names:
            js_func_files.append(
                (
                    f.name,
                    file_content,
                    re.compile(r"""(^|[='"\s\n])""" + func_name + r"\("),
                )
            )
    return js_func_files


class DocCompiler:
    js_func_files = get_js_func_files()

    def __init__(
        self,
        selector_styles: Optional[Dict[str, Dict[str, str]]] = None,
        js_files: Optional[List[Union[str, Path]]] = None,
        global_vars: Optional[Dict[str, Any]] = None,
    ):
        self.user_js_files = js_files or []
        self.global_vars = global_vars or {}
        self.selector_styles = defaultdict(dict)
        # initialize selector attributes with defaults.
        for selector, attributes in all_styles.items():
            self.add_selector_styles(selector, attributes)
        if selector_styles:
            # update with user-provided selector attributes.
            for selector, attributes in selector_styles.items():
                self.add_selector_styles(selector, attributes)

    def add_selector_styles(
        self,
        selector: str,
        attributes: Dict[str, Union[str, Callable]] = {},
        **kwarg_attributes,
    ):
        selectors = [s.strip() for s in selector.split(",")]
        for s in selectors:
            self.selector_styles[s].update(attributes)
            self.selector_styles[s].update(kwarg_attributes)

    def add_js_file(self, file: Union[str, Path]):
        self.user_js_files.append(file)

    def compile_header(self, doc: document):
        doc_html = doc.render()
        doc_tree = fromstring(doc_html)
        self._add_fonts(doc)

        if js := self._get_doc_js(doc_html):
            doc.head.add_raw_string(
                dedent(
                    f"""
                <script>
                    {js}
                </script>
            """
                )
            )

        if doc_styles := self._get_doc_styles(doc_tree, doc_html, js):
            doc.head.add_raw_string(
                dedent(
                    f"""
                <style>
                    {doc_styles}
                </style>
            """
                )
            )

    def _get_doc_js(self, doc_html: str) -> str:
        js = []
        if self.global_vars:
            global_vars = {
                k: f"'{v}'" if isinstance(v, str) else v for k, v in global_vars.items()
            }
            js.append("\n".join([f"var {k}={v};" for k, v in global_vars.items()]))
        if self.user_js_files:
            js.append(
                "\n".join([Path(f).read_text().strip() for f in self.user_js_files])
            )

        # add files for any functions used.
        files = {}
        for file_name, file_content, func_name_matcher in self.js_func_files:
            if any(func_name_matcher.search(j) for j in js) or func_name_matcher.search(
                doc_html
            ):
                files[file_name] = file_content
        if files:
            js.append("\n".join(files.values()))

        return "\n".join(js)

    def _get_doc_styles(self, doc_tree, doc_html, js) -> str:
        # Check if multiple selectors have the same values, and merge selectors into a comma-separated list.
        style_id_to_selectors = defaultdict(list)
        style_id_to_style = {}
        for selector, attributes in self.selector_styles.items():
            # make sure keys are ordered the same between dicts.
            style_id = tuple(sorted(attributes.items(), key=lambda x: x[0]))
            style_id_to_selectors[style_id].append(selector)
            style_id_to_style[style_id] = attributes
        selector_styles = {}
        for style_id, selectors in style_id_to_selectors.items():
            selector_styles[",\n".join(selectors)] = style_id_to_style[style_id]

        # parse document and determine what styles need to be added.
        doc_styles, matched_selectors = [], set()
        for selector, attributes in selector_styles.items():
            # clean selectors to base form. no pseudo-elements etc..
            base_selector = re.sub(
                r"(?<=[a-zA-Z])((\.|:|::).*?(?=(\s|$)))", "", selector
            )
            if (
                base_selector in matched_selectors
                or doc_tree.cssselect(base_selector)
                or re.search(
                    (
                        reg := r"classList\.(add|toggle)\('"
                        + re.escape(base_selector.lstrip("."))
                        + r"'\)"
                    ),
                    doc_html,
                )
                or re.search(reg, js)
            ):
                attributes = [
                    (k, f"{v};" if not v.endswith(";") else v)
                    for k, v in attributes.items()
                ]
                attributes = "".join([f"{k}: {v}" for k, v in attributes])
                doc_styles.append(
                    f"""{selector} {{
                        {attributes}  
                    }}
                """
                )
                matched_selectors.add(base_selector)
        return "\n".join([dedent(s) for s in doc_styles])

    def _add_fonts(self, doc: document):
        with doc.head:
            # fonts.
            d.link(rel="preconnect", href="https://fonts.googleapis.com")
            d.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="")
            d.link(
                rel="stylesheet",
                type="text/css",
                href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap",
            )
            # d.link(rel="stylesheet", href="https://fonts.googleapis.com/icon?family=Material+Icons")
            d.link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
            )
