document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const lightIcon = document.getElementById('light-icon');
    const darkIcon = document.getElementById('dark-icon');
    const htmlElement = document.documentElement;

    // Инициализация темы
    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        htmlElement.setAttribute('data-bs-theme', savedTheme);
        lightIcon.classList.toggle('d-none', savedTheme === 'dark');
        darkIcon.classList.toggle('d-none', savedTheme !== 'dark');
    }

    // Переключение темы
    function toggleTheme() {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        lightIcon.classList.toggle('d-none', newTheme === 'dark');
        darkIcon.classList.toggle('d-none', newTheme !== 'dark');
    }

    initTheme();
    themeToggle.addEventListener('click', toggleTheme);
});