// Auto-dismiss Django toast messages after 3 seconds using Vanilla JavaScript
document.addEventListener('DOMContentLoaded', () => {
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(toast => {
    // Wait 3 seconds (3000ms), then trigger smooth fade-out and slide-up transition
    setTimeout(() => {
      toast.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-12px)';
      setTimeout(() => {
        if (toast.parentNode) {
          toast.remove();
        }
      }, 600);
    }, 3000);
  });
});
