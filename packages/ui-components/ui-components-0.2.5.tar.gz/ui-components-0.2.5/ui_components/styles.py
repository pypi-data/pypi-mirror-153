tag_styles = {
    ":root": {
        "--off-black": "#212121;",
        "--light-grey": "#BDBDBD;",
        "--white-red": "#FFEBEE;",
        "--bright-green": "#7FFF00;",
        "--bright-blue": "#0310EA;",
        "--bright-purple": "#a544ff;",
        "--neon-yellow": "#F2EA02;",
        "--neon-red": "#FF3300;",
        "--neon-green": "#00FF66;",
        "--neon-blue": "#0062FF;",
        "--neon-pink": "#FF0099;",
        "--neon-purple": "#6E0DD0;",
    },
    "body": {
        "background": "var(--off-black);",
        "background-image": "linear-gradient(to right, var(--off-black), charcoal, var(--off-black));",
        "font-family": "'Poppins', sans-serif;",
    },
    "hr": {
        "border": "0;",
        "clear": "both;",
        "display": "block;",
        "background-color": "var(--neon-blue);",
        "height": "1px;",
    },
    "label": {
        "color": "var(--neon-blue);",
    },
    "select": {
        "background-color": "WhiteSmoke;",
        "color": "var(--off-black);",
        "font-size": "1.125em;",
    },
    "button, input[type=submit], input[type=reset]": {
        "background-color": "var(--bright-blue);",
        "color": "var(--off-black);",
        "border-radius": "5px;",
        "border": "2px solid var(--light-grey);",
        "transition-duration": "0.2s;",
        "cursor": "pointer;",
        "padding": "0.5em 1.33em;",
        "font-weight": "bold;",
    },
    "button:hover": {
        "background-color": "var(--neon-blue);",
    },
    "button.active": {
        "background-color": "var(--neon-blue);",
    },
    "table, th, td": {
        "border-left": "1px solid var(--neon-blue);",
        "border-right": "1px solid var(--neon-blue);",
        "text-align": "center;",
    },
    "table": {
        "display": "table;",
        "border-collapse": "collapse;",
        "width": "80%;",
        "border-bottom": "2px solid var(--neon-blue);",
    },
    "thead": {
        "background": "var(--neon-blue);",
    },
    "tbody tr:nth-child(odd)": {
        "background": "WhiteSmoke;",
    },
    "tbody tr:nth-child(even)": {
        "background": "white;",
    },
}

tab_styles = {
    ".tab": {
        "overflow": "hidden;",
        "border-radius": "0px;",
        "background-color": "Gainsboro;",
    },
    ".tablinks": {
        "border": "1px solid black;",
        "cursor": "pointer;",
        "padding": "0.25em 0.33em;",
        "transition": "0.3s;",
        "font-size": "1em;",
        "border-radius": "0px;",
        "float": "left;",
        "outline": "none;",
        "overflow": "hidden;",
    },
    ".tabcontent": {
        "display": "none;",
        "border": "1px solid var(--neon-blue);",
        "border-radius": "5px;",
        "padding": "1em 5em;",
    },
}

layout_styles = {
    # horizontally center everything in a central vertical column.
    ".y-axis-centered": {
        "display": "flex;",
        "flex-direction": "column;",
        "justify-content": "center;",
        "align-content": "center;",
        "align-items": "center;",
    },
    # evenly horizontally space all 1st children of each 1st child
    ".space-around-rows>*": {
        "display": "flex;",
        "flex-direction": "row;",
        "justify-content": "space-around;",
        "column-gap": "20px;",
    },
    # evenly horizontally space all 1st children of each 1st child and also add a vertical gap between 1st children.
    ".space-around-spaced-rows>*": {
        "display": "flex;",
        "flex-direction": "row;",
        "justify-content": "space-around;",
        "column-gap": "20px;",
        "margin-top": "20px;",
        "margin-bottom": "20px;",
    },
}


iframe_styles = {
    ".iframe-container": {
        "position": "relative;",
        "overflow": "hidden;",
        "width": "100%;",
        "padding-top": "56.25%;",  # 16:9 Aspect Ratio (divide 9 by 16 = 0.5625)
    },
    # Then style the iframe to fit in the container div with full height and width */
    ".responsive-iframe": {
        "position": "absolute;",
        "top": "0;",
        "left": "0;",
        "bottom": "0;",
        "right": "0;",
        "width": "100%;",
        "height": "100%;",
    },
}

ioinfobox_styles = {
    ".ioinfobox_container": {"border": "1px solid;"},
    ".ioinfobox_input": {
        "background-color": "#b9c2a8",
    },
    ".ioinfobox_meta": {"background-color": "#a4c567"},
    ".ioinfobox_output": {"background-color": "#99ca3c"},
}


# TODO change colors.
multiselect_styles = {
    ".ms-container": {
        "border": "1px solid var(--neon-purple);",
        # "padding": "0.125em;",
        # "max-width": "17%;",
        # "resize": "both;",
        # "overflow": "auto;",
    },
    ".ms-selections": {
        "display": "flex;",
        "flex-flow": "row wrap;",
    },
    ".ms-option": {
        "border-style": "dashed;",
        "border-width": "1px;",
        "border-color": "var(--neon-purple);",
        "background-color": "GhostWhite;",  # "var(--neon-blue);",
        "color": "var(--off-black);",
        "padding": "0.2em;",
        "cursor": "pointer;",
    },
    ".ms-highlighted": {"background-color": "blue"},
}

pagaination_styles = {
    ".pagination": {
        "display": "inline-block;",
    },
    ".pagination a": {
        "color": "var(--bright-blue);",
        "float": "left;",
        "padding": "8px 16px;",
        "text-decoration": "none;",
        "transition": "background-color .2s;",
    },
    ".pagination a.active": {
        "background-color": "var(--neon-blue);",
        "color": "white;",
        "border-radius": "2px;",
    },
    ".pagination a:hover:not(.active)": {
        "background-color": "var(--neon-blue);",
        "border-radius": "2px;",
    },
}

tooltip_styles = {
    ".tooltip": {
        "position": "relative;",
        "display": "inline-block;",
        "border-bottom": "1px dotted var(--neon-purple);",
    },
    ".tooltip .tooltiptext": {
        "visibility": "hidden;",
        "width": "120px;",
        "background-color": "var(--neon-green);",
        "color": "black;",
        "text-align": "center;",
        "border-radius": "6px;",
        "padding": "5px 0;",
        # Position the tooltip
        "position": "absolute;",
        "z-index": "1;",
        "bottom": "150%;",
        "left": "50%;",
        "margin-left": "-60px;",
    },
    ".tooltip .tooltiptext::after": {
        "content": '"";',
        "position": "absolute;",
        "top": "100%;",
        "left": "50%;",
        "margin-left": "-5px;",
        "border-width": "5px;",
        "border-style": "solid;",
        "border-color": "pink transparent transparent transparent;",
    },
    ".tooltip:hover .tooltiptext": {
        "visibility": "visible;",
    },
}

top_label_style = {
    ".top-label": {
        "display": "inline-block;",
        "margin": "0 auto;",
        "padding": "0px;",
        # "background-color": "#8ebf42;",
        # "text-align": "center;",
    }
}

centered_top_label_style = {
    ".centered-top-label": {**top_label_style[".top-label"], "text-align": "center;"}
}

buttons_style = {
    ".close-btn": {
        "width": "1%;",
        "height": "1%;",
        "position": "absolute;",
        "right": "-1px;",
        "z-index": "1000;",
        "float": "right;",
        "top": "1px;",
    }
}


all_styles = {
    **tag_styles,
    **tab_styles,
    **layout_styles,
    **iframe_styles,
    **ioinfobox_styles,
    **multiselect_styles,
    **pagaination_styles,
    **tooltip_styles,
    **top_label_style,
    **centered_top_label_style,
}


def flexbox_class(**kwargs):
    properties = {
        "display": "flex",
        "flex-flow": "column wrap",
        "justify-content": "center",
        "align-items": "center",
        "align-content": "center",
        "background-color": "#1ae8bf",
    }
    properties.update(kwargs)


def grid_class(**kwargs):
    parent_props = {
        "display": "grid",
        "place-items": "center",
        "grid-template-rows": "",
        "grid-template-columns": "",
    }
    child_props = {
        "display": "grid",
        "gap": "20px",
        "grid-row": "",
        "grid-column": "",
    }
