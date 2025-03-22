document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll("button");
    buttons.forEach(button => {
        button.addEventListener("mouseover", () => {
            button.style.transform = "scale(1.1)";
        });
        button.addEventListener("mouseout", () => {
            button.style.transform = "scale(1)";
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("select").forEach(select => {
        select.addEventListener("change", function () {
            this.closest("form").submit();
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    console.log("Dashboard loaded!");
});
