// MAKE A TABLE OF ALL THE BOOKS IN THE DATABASE
const showAllBooks = function() {
	let response = JSON.parse(this.response);
	
	var txt = "";
	txt += "<table><tr><th>ID</th><th>Title</th><th>ISBN</th><th>Author(s)</th><th>Publisher</th></tr>"
	for (x in response) {
		var authors = (response[x].Authors);
		var publishers = (response[x].Publishers);

		var author = [];
		var publisher = [];

		for (i in authors) {
			author += authors[i].name + ", ";
		}

		for (i in publishers) {
			publisher += publishers[i].name
		}

		txt += "<tr><td>" + response[x].id + "</td><td>" + response[x].title + "</td><td>" + response[x].isbn + "</td><td>" + author + "</td><td>" + publisher + "</td></tr>";
	}
	txt += "</table>";

	document.getElementById("output").innerHTML = txt;

}

// GET ALL THE BOOKS FROM THE DATABASE
const makeAPIQuery = function() {
	let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", showAllBooks);
    xhttp.open("GET", "http://127.0.0.1:3000/books?allEntities=true");
    xhttp.send();
}

makeAPIQuery();