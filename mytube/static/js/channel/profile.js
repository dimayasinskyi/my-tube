// Activates hidden input when clicking on the avatar.
const form = document.getElementById("channelForm");
document.getElementById("avatar-input").addEventListener("change", function (event) {
    const [file] = event.target.files;
    if (file) {
        const preview = document.querySelector("label[for='avatar-input'] img");
        preview.src = URL.createObjectURL(file);
    }
    form.submit();
});

// Activates hidden input when clicking on the banner.
document.getElementById("banner-input").addEventListener("change", function (event) {
    const [file] = event.target.files;
    if (file) {
        const preview = document.querySelector("label[for='banner-input'] img");
        preview.src = URL.createObjectURL(file);
    }
    form.submit()
})