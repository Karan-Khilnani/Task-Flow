// Theme switcher with localStorage persistence
const html = document.documentElement;
const btns = document.querySelectorAll('.theme-btn');

// Load saved theme
const savedTheme = localStorage.getItem('taskflow-theme') || 'light';
setTheme(savedTheme);

btns.forEach(btn => {
  btn.addEventListener('click', () => setTheme(btn.dataset.theme));
});

function setTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('taskflow-theme', theme);
  btns.forEach(b => b.classList.toggle('active', b.dataset.theme === theme));
}

// Auto-dismiss alerts
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => el.style.opacity = '0', 3500);
  setTimeout(() => el.remove(), 4000);
});