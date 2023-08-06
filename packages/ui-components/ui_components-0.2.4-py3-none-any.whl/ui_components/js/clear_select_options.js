function clear_select_options(select_id) {
    /* remove all options from a select element. */
    let select = document.getElementById(select_id);
    while (select.options.length > 0) {
        select.remove(0);
    }
}