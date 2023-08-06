
function get_box_positions() {
    let data = {
        'scrollX': window.scrollX,
        'scrollY': window.scrollY,
    }
    let positions = [];
    let boxes = document.querySelector('.ioinfobox_container');
    for (let box of boxes) {
        var rect = box.getBoundingClientRect();
        positions.push({
            left: rect.left + window.pageXOffset,
            top: rect.top + window.pageYOffset,
            width: rect.width || box.offsetWidth,
            height: rect.height || box.offsetHeight
        });
    }
    data['positions'] = positions;
    return data;
}