// Tracks pressing enter when changing searchInput.
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("commentForm")
    const searchInput = document.getElementById("commentInput");

    searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            form.submit()
        }
    });
});