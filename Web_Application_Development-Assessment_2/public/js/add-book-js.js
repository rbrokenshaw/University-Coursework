var responseIDPass = ""

// MAKE A SEARCH STRING
const encodeParameters = function(params) {
    var strArray = [];
    Object.keys(params).forEach(function(key) {
        var paramString = encodeURIComponent(key) + "=" + encodeURIComponent(params[key]);
        strArray.push(paramString);
    });
    return strArray.join("&");
};

// ADD PUBLISHER
const addPublisher = function(responseID) {
	var book_id = responseID;
	let book_publisher = document.getElementById("book_publisher").value;
	
	var xhttp4 = new XMLHttpRequest();
	var publisherUrl = "http://127.0.0.1:3000/books/" +book_id+ "/publishers";

    xhttp4.open("POST", publisherUrl);
    xhttp4.setRequestHeader('Content-Type', 'application/json');

	var params = {
		name: book_publisher
	};

	xhttp4.send(JSON.stringify(params));

	output.innerHTML = "New book sucessfully added, <a href='/add-book'>click here</a> to add another book.";
}

// ADD AUTHOR
const addAuthor = function(responseID) {
	var next = function() {
		let responseID = responseIDPass;
		addPublisher(responseID);
	}

	var book_id = responseID;
	let book_author = document.getElementById("book_author").value;
	
	var xhttp3 = new XMLHttpRequest();
	var authorUrl = "http://127.0.0.1:3000/books/" +book_id+ "/authors";

    xhttp3.open("POST", authorUrl);
    xhttp3.setRequestHeader('Content-Type', 'application/json');

	var params = {
		name: book_author
	};

	xhttp3.send(JSON.stringify(params));

	xhttp3.addEventListener("load", next)
}

// GET BOOK ID
const getID = function(book_isbn) {
	const idResponse = function() {
		let response = JSON.parse(this.response);
		let responseID = (response[0].id);
		addAuthor(responseID);
		responseIDPass += responseID; 
	};

	var xhttp2 = new XMLHttpRequest();

	var params = {
		isbn: book_isbn
	};

	var url = "http://127.0.0.1:3000/search?type=book&isbn=" + book_isbn;

	xhttp2.open("GET", url);
	xhttp2.addEventListener("load", idResponse);
	xhttp2.send();
}

// ADD TITLE AND ISBN
const addTitleAndISBN = function(book_title,book_isbn) {
	var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://127.0.0.1:3000/books");
    xhttp.setRequestHeader('Content-Type', 'application/json');

    var params = {
        title: book_title,
        isbn: book_isbn
    };
    
    xhttp.send(JSON.stringify(params));

    xhttp.onload = function() {
    	getID(book_isbn);
	};
}

// SUBMIT BUTTON
document.querySelector('#book_submit').addEventListener('click', function() {
	let book_title = document.getElementById("book_title").value;
	let book_isbn = document.getElementById("book_isbn").value;
	let book_author = document.getElementById("book_author").value;

	if (book_title === "") {
		alert("Please input a book title");
		return false;
	}

	if (book_isbn === "") {
		alert("Please input an ISBN");
		return false;
	}

	if (book_author === "") {
		alert("Please input an author");
		return false;
	}

	addTitleAndISBN(book_title,book_isbn);
});



