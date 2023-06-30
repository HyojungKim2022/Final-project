
var originalRows = []; // Store the original table rows

window.onload = function () {
    var table = document.querySelector(".stock");
    var rows = table.getElementsByTagName("tr");

    // Store the original table rows in the originalRows array
    for (var i = 1; i < rows.length; i++) {
        originalRows.push(rows[i]);
    }
};

function searchTable() {
    var input = document.getElementById("searchInput");
    var filter = input.value.toUpperCase();
    var table = document.querySelector(".stock");
    var rows = table.getElementsByTagName("tr");

    // Reset the table to the original rows
    for (var i = 1; i < rows.length; i++) {
        table.appendChild(originalRows[i - 1]);
    }

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var found = false;

        for (var j = 0; j < cells.length; j++) {
            var cell = cells[j];
            if (cell) {
                var cellText = cell.textContent || cell.innerText;
                if (cellText.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }

        if (found) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}