// Tracks pressing enter when changing searchInput.
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const baseUrl = searchInput.dataset.baseUrl;

    searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();

            const query = searchInput.value.trim();

            if (query) {
                window.location.href = `${baseUrl}?search=${encodeURIComponent(query)}`;
                searchInput.value = query;
            }
            else {
                window.location.href = baseUrl;
            }
        }
    });
});