// Clear search filter button
document.getElementById('clear-filter-btn').addEventListener("click", function() {
	window.location.href = window.location.href.split('results/?')[0];
})