// EstateIQ main.js

function toggleMenu() {
  const m = document.getElementById('mobileMenu');
  if (m) m.classList.toggle('open');
}

document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts
  document.querySelectorAll('.eq-alert').forEach(function (el) {
    setTimeout(function () { el.remove(); }, 4000);
  });
  // Close mobile menu on link click
  document.querySelectorAll('.mobile-menu a').forEach(function (a) {
    a.addEventListener('click', function () {
      const m = document.getElementById('mobileMenu');
      if (m) m.classList.remove('open');
    });
  });
});
