// When the user clicks on the button, scroll to the top of the document
let backToTop = document.getElementById("scroll-up");
let image = backToTop.getElementsByTagName("img")[0];
image.addEventListener("click", scrollToTop);

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

// When the user scrolls down 700px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 700 || document.documentElement.scrollTop > 700) {
        image.style.display = "block";
    } else {
        image.style.display = "none";
    }
}

// Reset search on browser "back button"
window.onload = function() {
	document.getElementById("search").value = '';
}

// Clear search filter button
document.getElementById('clear-filter-btn').addEventListener("click", function() {
	window.location.href = window.location.href.split('results/?')[0];
})