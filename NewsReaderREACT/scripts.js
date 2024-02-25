function toggleSubtabs() {
    const subtabs = document.querySelector('.subtabs');
    if (subtabs.style.display === 'none' || subtabs.style.display === '') {
        subtabs.style.display = 'block';
    } else {
        subtabs.style.display = 'none';
    }
}

function loadNews(sport) {
    // You can customize this function to load news articles based on the selected sport
    // For demonstration purposes, let's log the selected sport to the console
    console.log('Selected sport:', sport);
}
