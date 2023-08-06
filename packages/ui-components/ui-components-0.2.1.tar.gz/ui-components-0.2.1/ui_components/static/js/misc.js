

function title_case(str) {
    /* convert a string to title case */
    str = str.replace('_', ' ').split(' ');
    for (var i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
    }
    return str.join(' ');
}

function clear_select_options(select_id) {
    /* remove all options from a select element. */
    let select = document.getElementById(select_id);
    while (select.options.length > 0) {
        select.remove(0);
    }
}

function set_select_options(select_id, options) {
    if (options) {
        let select = document.getElementById(select_id);
        options.forEach(value => {
            let option = document.createElement('option');
            option.appendChild(document.createTextNode(value));
            option.setAttribute('value', value);
            select.appendChild(option);
        });
    }
}


function switch_tab(event, active_tab_id) {
    let i, tabcontent, tablinks;

    // This is to clear the previous clicked content.
    tabcontent = document.getElementsByClassName('tabcontent');
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }

    // Set the tab to be 'active'.
    tablinks = document.getElementsByClassName('tablinks');
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(' active', '');
    }

    // Display the clicked tab and set it to active.
    document.getElementById(active_tab_id).style.display = 'block';
    event.currentTarget.className += ' active';
}

