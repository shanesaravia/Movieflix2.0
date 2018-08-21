// Reset search on browser "back button"
window.onload = function() {
	document.getElementById("search").value = '';
}

// load local cache data
function loadCache(key) {
	let cache = localStorage[key] || "{}";
	return JSON.parse(cache);
}

function getValFromCache(cache, key) {
	return cache[key] || 0
}

function saveValToCache(cache, title, val, webCacheKey) {
	cache[title] = val;
	localStorage[webCacheKey] = JSON.stringify(cache);
	return true;
}

function filterInt(strval) {
	if (strval.includes("k")) {
		strval = strval.replace("k", "000");
		return parseInt(strval);
	} else {
		return parseInt(strval);
	}
}

function syncDbLikesDislikes(title, field, action) {
	$.ajax({
        url: "/updateLikesDislikes",
        data : {"movie": title, "field": field, "action": action},
        success : function(status) {
        	console.log(status)
        }
    })
}

// function updateCache(item) {
// 	// Check cache for thumbs up/down
// 	let title = item.closest(".movie-box").getElementsByClassName("movie-title")[0].textContent
// 	let val;
// 	val = getValFromCache(likesData, )
// 	val = (val ? 0 : 1);
// 	likesData[title] = val
// 	localStorage['localLikes'] = JSON.stringify(likesData)
// }

// Assign state to likes and dislikes from cache on page load
function applyState(movie, cls, cache, prop) {
	obj = movie.getElementsByClassName(cls)[0];
	title = movie.getElementsByClassName("movie-title")[0].textContent;
	state = getValFromCache(cache, title);
	movie.title = title;
	movie[prop] = state;
	if (state) {
		obj.classList.remove(cls);
	}
}

// Mini-bar click
function activateCounter(movie, el, prop, cache, webCacheKey) {
	obj = movie.getElementsByClassName(el)[0];
	obj.addEventListener("click", function(e) {
		let amount = this.getElementsByTagName("span")[0]
		let thumbsFull = this.getElementsByTagName("img")[1];

		if (movie[prop]) {
			// Adjust num, remove thumbs-full
			if (amount.textContent.includes("k") === false) {
				amount.textContent--;
			}
			thumbsFull.classList.add(prop + "-alt");
			syncDbLikesDislikes(movie.title, prop, "remove")
		} else {
			// Adjust num, add thumbs-full
			if (amount.textContent.includes("k") === false) {
				amount.textContent++
			}
			thumbsFull.classList.remove(prop + "-alt");
			syncDbLikesDislikes(movie.title, prop, "add")
		}
		movie[prop] = (movie[prop] ? 0 : 1);
		saveValToCache(cache, movie.title, movie[prop], webCacheKey);
		e.preventDefault();
	})
}

function prepareMovies(el){
	for (movie of el) {
		// check cache to have image full or not
		applyState(movie, "likes-alt", likesCache, "likes");
		applyState(movie, "dislikes-alt", dislikesCache, "dislikes");
		activateCounter(movie, "likes-container", "likes", likesCache, "localLikes");
		activateCounter(movie, "dislikes-container", "dislikes", dislikesCache, "localDislikes");
	}
};


likesCache = loadCache("localLikes");
dislikesCache = loadCache("localDislikes");

movieBox = document.getElementsByClassName("movie-box")
prepareMovies(movieBox);




// for (i of likes) {
// 	i.addEventListener("click", function(e) {
// 		alert("working!");
// 		e.preventDefault();
// 	})
// }

// function likesClick(likes) {
// 	for (i of likes) {
// 		i.addEventListener("click", function(event) {
// 			alert("working!");

// 		})
// 	}
// }

// likesClick(likes);


// for (i of likes) {
// 	i.addEventListener("click", function() {
// 		alert("working!");
// 		let e = window.event;
// 		e.cancelBubble = true;
// 		e.stopPropagation();
// 	})
// }

// {
//     if (!e) var e = window.event;
//     e.cancelBubble = true;
//     if (e.stopPropagation) e.stopPropagation();
// }

// Change mini-bar icons on hover
// function updateOnHover(className, imageUrlOn, imageUrlOff) {
// 	for (i of className) {
// 		i.addEventListener("mouseover", function() {
// 			this.src = imageUrlOn
// 		})
// 		i.addEventListener("mouseout", function() {
// 			this.src = imageUrlOff
// 		})
// 	}
// }

// imageRoot = '/static/images/';
// likes = document.getElementsByClassName("like");
// dislikes = document.getElementsByClassName("dislike");
// favorites = document.getElementsByClassName("favorite");

// likesSpan = document.getElementsByClassName("likes")

// // updateOnHover(likes, `${imageRoot}thumbs-up-icon-full.png`, `${imageRoot}thumbs-up-icon.png`);
// updateOnHover(dislikes, `${imageRoot}thumbs-down-icon-full.png`, `${imageRoot}thumbs-down-icon.png`);
// updateOnHover(favorites, `${imageRoot}star-icon-full.png`, `${imageRoot}star-icon.png`);

// updateOnHover(likesSpan, `${imageRoot}thumbs-up-icon-full.png`, `${imageRoot}thumbs-up-icon.png`);