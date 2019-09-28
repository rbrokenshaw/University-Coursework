// DELETE A LOAN FROM THE DATABASE
const deleteLoan = function(id,bookID) {
    let loan_id = id;
    let book_id = bookID

        if (confirm('Are you sure you want to return this book? Click "OK" to proceed.')) {
            var loan_url = "http://127.0.0.1:3000/loans/" + loan_id
            var xhttp = new XMLHttpRequest();

            xhttp.open("DELETE", loan_url);
            xhttp.send();

            var outputDiv = document.getElementById("output4");
            outputDiv.innerHTML = "Book with ID " + book_id + " successfully returned.";
        } else {
            return false;
        }

}

// MAKE A TABLE OF THE USER'S LOANS
const makeLoanTable = function() {
	let response = JSON.parse(this.response);

	var loansListP = document.createElement("P");
	var loansListPText = document.createTextNode("Here are the selected user's current loans:");
	loansListP.appendChild(loansListPText);


	var txt = "";
	txt += "<table><tr><th>Book ID</th><th>Due Date</th><th>Return Book</th></tr>"
	for (x in response) {
		txt += "<tr><td>" + response[x].BookId + "</td><td>" + response[x].dueDate.substring(0,10) + "</td><td><input type='button' onclick='deleteLoan(" + response[x].id + "," + response[x].BookId + ")' value='Return Book'></td></tr>";
	}
	txt += "</table>";

	var outputDiv = document.getElementById("output2");
	outputDiv.appendChild(loansListP);

	document.getElementById("output3").innerHTML = txt;


}

// GET THE SELECTED USER'S LOANS
const selectUser = function(userID) {
	var url = "http://127.0.0.1:3000/users/" + userID + "/loans";

	var xhttp = new XMLHttpRequest();
	xhttp.addEventListener("load", makeLoanTable);
    xhttp.open("GET", url);
    xhttp.send();
}


// MAKE A TABLE OF MATCHED USERS
const makeTable = function() {
	let response = JSON.parse(this.response);

	var txt = "";
	txt += "<table><tr><th>ID</th><th>Name</th><th>Barcode</th><th>Choose?</th></tr>";
	for (x in response) {
		txt += "<tr><td>" + response[x].id + "</td><td>" + response[x].name + "</td><td>" + response[x].barcode + "</td><td><input type='button' onclick='selectUser(" + response[x].id + ")' value='Select User'></td></tr>"	
	}
	txt += "</table>";

	document.getElementById("output").innerHTML = txt;

	if (response.length === 0) {
		var noMatches = "Sorry, there are no matches."
		document.getElementById("output").innerHTML = noMatches;
	};
};

// MAKE A SEARCH STRING
const encodeParameters = function(params) {
    var strArray = [];
    Object.keys(params).forEach(function(key) {
        var paramString = encodeURIComponent(key) + "=" + encodeURIComponent(params[key]);
        strArray.push(paramString);
    });
    return strArray.join("&");
};

//SEARCH FOR A USER
const makeAPIQuery = function(search_term) {
    let rootURL = "http://127.0.0.1:3000/search";

    var barcodeNum = parseInt(search_term, 10)

    //If the user inputs an integer, search the barcode field
    if (Number.isInteger(barcodeNum)) {
        var params = {
            barcode: search_term
        };
    } else {
        var params = {
            name: search_term
        };
    };

    let queryURL = rootURL + "?type=user&" + encodeParameters(params);

    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", makeTable);
    xhttp.open("GET", queryURL);
    xhttp.send();
};

// SEARCH BUTTON
let submitButton = document.getElementById("view_user_loans_button");
submitButton.addEventListener("click", function() {
    let search_term = document.getElementById("search_term").value;

    if (search_term) {
        makeAPIQuery(search_term);
    };

    if (search_term == "") {
        alert("Please enter a search term.");
        return false;
    };
});