const toggleButton = document.getElementById('toggle-button');
const body = document.body;
const toggleButtonText = toggleButton.innerText;

// Load the saved theme from localStorage
const currentTheme = localStorage.getItem('theme');
if (currentTheme && currentTheme === 'dark') {
    body.classList.add('dark-mode');
    toggleButton.innerText = 'Day'; // Update button text to "Day"
} else {
    toggleButton.innerText = 'Night'; // Default to "Night"
}

// Toggle dark/light mode and save the preference in localStorage
toggleButton.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    
    // Change button text based on current theme
    if (body.classList.contains('dark-mode')) {
        toggleButton.innerText = 'Day'; // Show "Day" when dark mode is active
    } else {
        toggleButton.innerText = 'Night'; // Show "Night" when light mode is active
    }

    // Save the current theme preference in localStorage
    const theme = body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
});


