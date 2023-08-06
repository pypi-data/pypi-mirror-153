function title_case(str) {
    /* convert a string to title case */
    str = str.replace('_', ' ').split(' ');
    for (var i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
    }
    return str.join(' ');
}