

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