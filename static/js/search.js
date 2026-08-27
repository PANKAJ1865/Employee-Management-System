// Standard JavaScript for Live Table Filtering and Column Sorting

function initLiveSearch() {
  var searchInput = document.getElementById('liveSearchInput');
  var table = document.querySelector('.custom-table');
  if (!searchInput || !table) return;

  var tableBody = table.querySelector('tbody');
  if (!tableBody) return;

  var noResultsRow = document.getElementById('noLiveResultsRow');
  if (!noResultsRow) {
    noResultsRow = document.createElement('tr');
    noResultsRow.id = 'noLiveResultsRow';
    noResultsRow.style.display = 'none';
    noResultsRow.innerHTML = '<td colspan="8" style="text-align: center; padding: 2.5rem; color: var(--text-muted);"><p style="font-size: 1.05rem; margin-bottom: 0.25rem; font-weight: 600;">No matching employees found</p><p style="font-size: 0.85rem;">No employee matches your search criteria. Try a different name, department, or designation.</p></td>';
    tableBody.appendChild(noResultsRow);
  }

  searchInput.oninput = function(e) {
    var term = e.target.value.toLowerCase().trim();
    var rows = tableBody.querySelectorAll('tr:not(#noLiveResultsRow)');
    var visibleCount = 0;

    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      var nameEl = row.querySelector('.emp-name');
      var deptEl = row.querySelector('.badge-dept');
      var desigText = row.cells[4] ? row.cells[4].textContent.toLowerCase() : '';

      var nameText = nameEl ? nameEl.textContent.toLowerCase() : '';
      var deptText = deptEl ? deptEl.textContent.toLowerCase() : '';
      var fullRowText = row.textContent.toLowerCase();

      if (term === '' || nameText.indexOf(term) !== -1 || deptText.indexOf(term) !== -1 || desigText.indexOf(term) !== -1 || fullRowText.indexOf(term) !== -1) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    }

    if (noResultsRow) {
      noResultsRow.style.display = (visibleCount === 0 && rows.length > 0) ? '' : 'none';
    }
  };
}

function initTableSorting() {
  var table = document.querySelector('.custom-table');
  if (!table) return;

  var tableBody = table.querySelector('tbody');
  var sortableHeaders = table.querySelectorAll('th.sortable');

  for (var i = 0; i < sortableHeaders.length; i++) {
    (function(header) {
      header.style.cursor = 'pointer';
      header.title = 'Click to sort ascending / descending';

      header.onclick = function() {
        var colIdx = parseInt(header.getAttribute('data-col-idx'), 10);
        var sortType = header.getAttribute('data-sort-type');
        var currentDir = header.getAttribute('data-sort-dir') === 'asc' ? 'desc' : 'asc';

        for (var j = 0; j < sortableHeaders.length; j++) {
          sortableHeaders[j].removeAttribute('data-sort-dir');
          var icon = sortableHeaders[j].querySelector('.sort-icon');
          if (icon) icon.textContent = '↕';
        }

        header.setAttribute('data-sort-dir', currentDir);
        var currentIcon = header.querySelector('.sort-icon');
        if (currentIcon) currentIcon.textContent = currentDir === 'asc' ? '▲' : '▼';

        var rowsArray = [];
        var rows = tableBody.querySelectorAll('tr:not(#noLiveResultsRow)');
        for (var k = 0; k < rows.length; k++) {
          rowsArray.push(rows[k]);
        }

        rowsArray.sort(function(a, b) {
          var valA = a.cells[colIdx] ? a.cells[colIdx].textContent.trim() : '';
          var valB = b.cells[colIdx] ? b.cells[colIdx].textContent.trim() : '';

          if (sortType === 'number') {
            var numA = parseFloat(valA.replace(/[^0-9.-]+/g, '')) || 0;
            var numB = parseFloat(valB.replace(/[^0-9.-]+/g, '')) || 0;
            return currentDir === 'asc' ? numA - numB : numB - numA;
          } else if (sortType === 'date') {
            var dateA = new Date(valA).getTime() || 0;
            var dateB = new Date(valB).getTime() || 0;
            return currentDir === 'asc' ? dateA - dateB : dateB - dateA;
          } else {
            return currentDir === 'asc'
              ? valA.localeCompare(valB, undefined, { numeric: true, sensitivity: 'base' })
              : valB.localeCompare(valA, undefined, { numeric: true, sensitivity: 'base' });
          }
        });

        var noResultsRow = document.getElementById('noLiveResultsRow');
        for (var m = 0; m < rowsArray.length; m++) {
          if (noResultsRow) {
            tableBody.insertBefore(rowsArray[m], noResultsRow);
          } else {
            tableBody.appendChild(rowsArray[m]);
          }
        }
      };
    })(sortableHeaders[i]);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    initLiveSearch();
    initTableSorting();
  });
} else {
  initLiveSearch();
  initTableSorting();
}
