document.addEventListener("DOMContentLoaded", function() {
    const table = document.getElementById('favouritesTable');
    const headers = table.querySelectorAll('th');
    let sortDirection = 1; // 1 for ascending, -1 for descending
    let lastSortedColumn = null;
  
    // Get all headers and their respective indexes
    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            if (lastSortedColumn === index) {
                // If clicking the same column, toggle sort direction
                sortDirection *= -1;
            } else {
                // If new column, reset to ascending
                sortDirection = 1;
                lastSortedColumn = index;
            }
  
            // Reset sorting classes for all headers
            headers.forEach(h => {
                h.classList.remove('asc', 'desc', 'sorted');
            });
  
            // Add the right class to the sorted header
            header.classList.add('sorted', sortDirection === 1 ? 'asc' : 'desc');
  
            sortTableByColumn(table, index, sortDirection);
        });
    });
   
    function sortTableByColumn(table, column, direction) {
        // Getting the first, and only, tbody in the table
        const tbody = table.tBodies[0];
        const rowsArray = Array.from(tbody.querySelectorAll('tr'));
  
        // 'Drive Bars' is the 2nd column (index 1)
        const isNumericColumn = column === 1;
  
        rowsArray.sort((rowA, rowB) => {
            const cellA = rowA.cells[column].innerText.trim();
            const cellB = rowB.cells[column].innerText.trim();
  
            if (isNumericColumn) {
                const numA = parseInt(cellA, 10);
                const numB = parseInt(cellB, 10);
                return (numA - numB) * direction;  // Multiply by direction for ascending/descending
            } else {
                return cellA.localeCompare(cellB) * direction;  // For text comparison
            }
        });
  
        rowsArray.forEach(row => tbody.appendChild(row));  // Re-append rows to sort
    }
  });