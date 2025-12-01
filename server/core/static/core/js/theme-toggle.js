(function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;
    
    // Get saved theme or default to light
    function getSavedTheme() {
        return localStorage.getItem('theme') || 'light';
    }
    
    // Apply theme
    function applyTheme(theme) {
        if (theme === 'dark') {
            html.setAttribute('data-theme', 'dark');
            if (themeIcon) {
                themeIcon.className = 'bi bi-sun-fill';
            }
        } else {
            html.removeAttribute('data-theme');
            if (themeIcon) {
                themeIcon.className = 'bi bi-moon-fill';
            }
        }
        localStorage.setItem('theme', theme);
    }
    
    // Toggle theme
    function toggleTheme() {
        const currentTheme = getSavedTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    }
    
    // Initialize theme on page load
    applyTheme(getSavedTheme());
    
    // Add event listener
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
})();
