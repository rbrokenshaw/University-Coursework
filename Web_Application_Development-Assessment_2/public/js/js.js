function toggleMenu() {
    var x = document.getElementById("mobile-menu");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    };


    window.addEventListener("resize", function() {
        if (window.matchMedia("(min-width: 700px)").matches) {
            x.style.display = "none"
        } 
    });
}

