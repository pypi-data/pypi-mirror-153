
function add_option(container_id) {
    option_text = document.getElementById('user_option').value;
    if (!option_text) {
        console.log('No text provided. Can not add empty string as option.');
        return
    }
    for (ele of document.querySelectorAll('div#' + container_id + ' > div')) {
        if (ele.innerText == option_text) {
            console.log('Option already exists. Can not add duplicate option.');
            return
        }
    }
    option = document.createElement('span');
    option.classList.add('selection_option');
    option.onmousedown = (event) => {
        event.target.classList.toggle('highlighted_selection');
    }
    option.appendChild(document.createTextNode(option_text));
    document.getElementById(container_id).appendChild(option);
}
