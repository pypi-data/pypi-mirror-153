
function get_ms_options(id = null, only_selected = true) {
    var path = ""
    if (id) {
        path += 'div.ms-container';
    }
    else {
        path += "div#" + id
    }
    path += ' span.ms-option'
    if (only_selected) {
        path += '.ms-highlighted'
    }
    const option_eles = document.querySelectorAll(path);
    let options = [];
    for (const op of option_eles) {
        options.push(op.innerText);
    }
    return options
}