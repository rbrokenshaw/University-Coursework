// MAKE A TABLE OF ALL USERS IN THE DATABASE
const showAllUsers = function() {
	let response = JSON.parse(this.response);
	
	var txt = "";
	txt += "<table><tr><th>ID</th><th>Name</th><th>Barcode</th><th>Member Type</th></tr>"
	for (x in response) {
		txt += "<tr><td>" + response[x].id + "</td><td>" + response[x].name + "</td><td>" + response[x].barcode + "</td><td>" + response[x].memberType + "</td></tr>";
	}
	txt += "</table>";

	document.getElementById("output").innerHTML = txt;

}

// GET ALL THE USERS IN THE DATABASE
const makeAPIQuery = function() {
	let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", showAllUsers);
    xhttp.open("GET", "http://127.0.0.1:3000/users");
    xhttp.send();
}

makeAPIQuery();