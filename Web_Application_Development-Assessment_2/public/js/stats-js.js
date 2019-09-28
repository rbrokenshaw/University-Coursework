// COUNT AND OUTPUT THE NUMBER OF BOOKS IN THE DATABASE
const bookCount = function() {
	let response = JSON.parse(this.response);
	
	let bCount = response.length;

	let bookOutputDiv = document.getElementById("book_output");
	let bookP = document.createElement("P");
	let bookPText = document.createTextNode(bCount)
	bookP.appendChild(bookPText);
	bookOutputDiv.appendChild(bookP);

}


// COUNT AND OUTPUT THE NUMBER OF USERS IN THE DATABASE
const userCount = function() {
	let response = JSON.parse(this.response);
	
	let uCount = response.length;

	let userOutputDiv = document.getElementById("user_output");
	let userP = document.createElement("P");
	let userPText = document.createTextNode(uCount)
	userP.appendChild(userPText);
	userOutputDiv.appendChild(userP);

}

// COUNT AND OUTPUT THE NUMBER OF LOANS IN THE DATABASE
const loanCount = function() {
	let response = JSON.parse(this.response);
	
	let lCount = response.length;

	let loanOutputDiv = document.getElementById("loan_output");
	let loanP = document.createElement("P");
	let loanPText = document.createTextNode(lCount)
	loanP.appendChild(loanPText);
	loanOutputDiv.appendChild(loanP);
}

// GET ALL THE BOOKS IN THE DATABASE
const makeBookAPIQuery = function() {
	let xhttp1 = new XMLHttpRequest();
    xhttp1.addEventListener("load", bookCount);
    xhttp1.open("GET", "http://127.0.0.1:3000/books?allEntities=true");
    xhttp1.send();
}

// GET ALL THE USERS IN THE DATABASE
const makeUserAPIQuery = function() {
	let xhttp2 = new XMLHttpRequest();
    xhttp2.addEventListener("load", userCount);
    xhttp2.open("GET", "http://127.0.0.1:3000/users?allEntities=true");
    xhttp2.send();
}

// GET ALL THE LOANS IN THE DATABASE
const makeLoanAPIQuery = function() {
	let xhttp3 = new XMLHttpRequest();
    xhttp3.addEventListener("load", loanCount);
    xhttp3.open("GET", "http://127.0.0.1:3000/loans");
    xhttp3.send();
}

makeBookAPIQuery();
makeUserAPIQuery();
makeLoanAPIQuery();