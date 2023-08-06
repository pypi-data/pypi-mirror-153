
function activate_page_table(pg_no, table_id) {
    var num_tbody = document.getElementById(table_id).tBodies.length;
    // set new active.
    for (var p = 0; p < num_tbody; p++) {
        if (p == pg_no) {
            document.getElementById('pg' + p).style.display = 'table-row-group';
            document.getElementById('pag' + p).className = 'active';
        }
        else {
            document.getElementById('pg' + p).style.display = 'none';
            document.getElementById('pag' + p).className = '';
        }
    }
}

function set_pagination(page_count, table_id) {
    var pagination_id = table_id + '-pagination'
    var pagination = document.getElementById(pagination_id)
    // check if pages should be added or removed.
    var current_page_count = pagination.childElementCount;
    var pages_to_add = page_count - current_page_count;
    if (pages_to_add > 0) {
        var links = document.createDocumentFragment();
        for (let p = current_page_count; p < page_count; p++) {
            a = document.createElement('a')
            a.id = 'pag' + p
            a.onclick = function () { activate_page_table(p, table_id); };
            a.text = p + 1
            a.href = '#'
            links.appendChild(a);
        }
        pagination.appendChild(links);
    }
    else if (pages_to_add < 0) {
        // currently too many pages, so remove some.
        while (pages_to_add++ < 0) {
            pagination.removeChild(pagination.lastElementChild)
        }
    }
}

function load_table_header(table, header) {
    var thead = document.createElement('thead');
    table.appendChild(thead);
    var table_header = thead.insertRow()
    for (let col_name of header) {
        var cell = table_header.insertCell();
        cell.appendChild(document.createTextNode(col_name));
    }
}

function load_table_body(table, rows, rows_per_page, table_id) {
    // calculate the number paginated table bodies that are needed.
    var page_count = Math.ceil(rows.length / rows_per_page);
    // make sure the correct number of pagination links are shown.
    set_pagination(page_count, table_id);
    // load data for each page.
    for (var p = 0; p < page_count; ++p) {
        // add this page's tbody to table.
        var tbody = document.createElement('tbody');
        tbody.id = 'pg' + p;
        tbody.style.display = 'none';
        table.appendChild(tbody);
        // insert rows into tbody.
        var page_rows = rows.splice(0, rows_per_page);
        for (let row_data of page_rows) {
            var row = tbody.insertRow()
            for (let col_val of row_data) {
                var cell = row.insertCell();
                cell.appendChild(document.createTextNode(col_val));
            }
        }
        // set table 1 to display immediately.
        if (p == 0) {
            activate_page_table(p, table_id);
        }
    }
}

function load_table(rows, rows_per_page, table_id) {
    var table = document.getElementById(table_id);
    // clear any existing.
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
    // first row should be header and the rest should be data.
    header = rows.shift();
    load_table_header(table, header);
    load_table_body(table, rows, rows_per_page, table_id);
}