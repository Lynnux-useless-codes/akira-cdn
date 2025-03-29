document.addEventListener('DOMContentLoaded', function() {
    const modeToggleBtn = document.getElementById('mode-toggle');
    const bodyElement = document.body;

    // Check if the user's dark mode preference is already set in localStorage
    const isDarkModeEnabled = localStorage.getItem('darkModeEnabled');

    // Apply the dark mode class if the preference is set or saved
    if (isDarkModeEnabled === 'true') {
        bodyElement.classList.add('dark-mode');
        // Update the icon to sunny when dark mode is enabled
        modeToggleBtn.innerHTML = '<ion-icon name="sunny-outline"></ion-icon>';
    }

    modeToggleBtn.addEventListener('click', function() {
        // Toggle the dark mode class on the body element
        bodyElement.classList.toggle('dark-mode');

        // Update the icon based on the current mode
        const isCurrentlyDarkMode = bodyElement.classList.contains('dark-mode');
        modeToggleBtn.innerHTML = isCurrentlyDarkMode ? '<ion-icon name="sunny-outline"></ion-icon>' : '<ion-icon name="moon-outline"></ion-icon>';

        // Save the dark mode preference in localStorage
        localStorage.setItem('darkModeEnabled', isCurrentlyDarkMode.toString());
    });
});
