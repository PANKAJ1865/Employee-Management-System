// Client-side interactions for Employee Management System
document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss toast messages after 4 seconds
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(toast => {
    setTimeout(() => {
      toast.style.transition = 'opacity 0.5s ease';
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 500);
    }, 4000);
  });

  // Client-side live table filter search
  const searchInput = document.getElementById('tableSearchInput');
  const tableRows = document.querySelectorAll('.custom-table tbody tr');

  if (searchInput && tableRows.length > 0) {
    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase().trim();
      tableRows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }
});
