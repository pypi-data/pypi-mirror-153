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


def compile_document(
    doc: document,
    selector_styles: Optional[Dict[str, Dict[str, str]]] = None,
    js_files: Optional[List[Union[str, Path]]] = None,
    global_vars: Optional[Dict[str, Any]] = None,
):
    user_selector_styles = selector_styles or {}
    user_js_files = js_files or []
    user_global_vars = global_vars or {}

    # add fonts and icons.
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

    # load document for parsing.
    doc_html = doc.render()
    doc_tree = fromstring(doc_html)

    ## add JavaScript. ##
    js = []
    if user_global_vars:
        user_global_vars = {
            k: f"'{v}'" if isinstance(v, str) else v
            for k, v in user_global_vars.items()
        }
        js.append("\n".join([f"var {k}={v};" for k, v in user_global_vars.items()]))
    if user_js_files:
        js.append("\n".join([Path(f).read_text().strip() for f in user_js_files]))

    # add files for any functions used.
    files = {}
    for file_name, file_content, func_name_matcher in get_js_func_files():
        if any(func_name_matcher.search(j) for j in js) or func_name_matcher.search(
            doc_html
        ):
            files[file_name] = file_content
    if files:
        js.append("\n".join(files.values()))
    if js := "\n".join(js):
        doc.head.add_raw_string(
            dedent(
                f"""
            <script>
                {js}
            </script>
        """
            )
        )
    ## Add CSS ##
    selector_styles = defaultdict(dict)

    def add_selector_styles(
        selector: str,
        attributes: Dict[str, Union[str, Callable]] = {},
    ):
        selectors = [s.strip() for s in selector.split(",")]
        for s in selectors:
            selector_styles[s].update(attributes)

    # initialize selector attributes with defaults.
    for selector, attributes in all_styles.items():
        add_selector_styles(selector, attributes)
    if selector_styles:
        # update with user-provided selector attributes.
        for selector, attributes in user_selector_styles.items():
            add_selector_styles(selector, attributes)

    # check if multiple selectors have the same values, and merge selectors into a comma-separated list.
    style_id_to_selectors = defaultdict(list)
    style_id_to_style = {}
    for selector, attributes in selector_styles.items():
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
        base_selector = re.sub(r"(?<=[a-zA-Z])((\.|:|::).*?(?=(\s|$)))", "", selector)
        if (
            # skip if selector has already been processed.
            base_selector in matched_selectors
            # check for elements at selector paths.
            or doc_tree.cssselect(base_selector)
            # check for classes used in JavaScript.
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
    if doc_styles:
        doc_styles = "\n".join([dedent(s) for s in doc_styles])
        doc.head.add_raw_string(
            dedent(
                f"""
            <style>
                {doc_styles}
            </style>
        """
            )
        )
