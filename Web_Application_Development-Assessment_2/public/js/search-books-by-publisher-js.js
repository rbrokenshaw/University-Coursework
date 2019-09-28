let bookIDList = [];
let onLoanIDList = [];


// MAKE A TABLE OF LOAN DETAILS FOR A BOOK
const makeLoanTable = function(response) {
    var tabletxt = "";

    tabletxt += "<table><tr><th>Loan ID</th><th>Book ID</th><th>User ID</th><th>Due Date</th></tr><tr><td>" + response.id + "</td><td>" + response.BookId + "</td><td>" + response.UserId + "</td><td>" + response.dueDate.substring(0,10) + "</td></tr></table>";

    let outputDiv = document.getElementById("loan_output");
    outputDiv.innerHTML = tabletxt;
}

// SHOW THE USER THE LOAN DETAILS OR INFORM THAT A BOOK IS AVAILABLE TO BORROW
const makeLoanRequest = function(book_id) {
    let getRequestResponse = function() {
        let response = JSON.parse(this.response);
        
        for (z in response) {
            if (response[z].BookId == book_id) {
                makeLoanTable(response[z]);
            };
        };        
};
    
    if (bookIDList.includes(book_id)) {
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:3000/loans")
        xhttp.send();
        xhttp.addEventListener("load", getRequestResponse);
    } else {
        let noLoanP = document.createElement("P");
        let noLoanPText = document.createTextNode("The book with ID " + book_id + " is currently available to borrow.");
        noLoanP.appendChild(noLoanPText);

        let outputDiv = document.getElementById("loan_output2");
        outputDiv.appendChild(noLoanP);
    };
}

// CHECK IF A BOOK IS ON LOAN
const getLoans = function(book_id) {
    onLoanIDList =+ book_id;
    var result = bookIDList.includes(onLoanIDList);

    if (result) {
        return "On Loan"
    } else {
        return "Not On Loan"
    };
};

// GET A LIST OF THE BOOK IDS OF THE BOOKS THAT ARE ON LOAN
const getLoanList = function() {
    var xhttp2 = new XMLHttpRequest();
    xhttp2.open("GET", "http://127.0.0.1:3000/loans");
    xhttp2.send();
    xhttp2.onload = function() {
        let response = JSON.parse(this.response);
        for (x in response) {
            bookIDList.push(response[x].BookId);
        }
    };
};

// DELETE A BOOK FROM THE DATABASE
const deleteButton = function(id) {
    let book_id = id;

    if (confirm('Are you sure you want to delete this book? Click "OK" to proceed.')) {
        var book_url = "http://127.0.0.1:3000/books/" + book_id
        var xhttp = new XMLHttpRequest();

        xhttp.open("DELETE", book_url);
        xhttp.send();

        var outputDiv = document.getElementById("update_output");

        var successP = document.createElement("P");
        var successPText =document.createTextNode("Book wth id " + book_id + " successfully deleted.");
        successP.appendChild(successPText);
        outputDiv.appendChild(successP);

        refreshButton = document.createElement("BUTTON");
        refreshButtonText = document.createTextNode("Refresh Results");
        refreshButton.appendChild(refreshButtonText);

        let outputDiv2 = document.getElementById("refresh_output");
        outputDiv2.appendChild(refreshButton);

        refreshButton.addEventListener("click", function() {
            let search_term = document.getElementById("search_term").value;
            makeAPIQuery(search_term);
        })

    } else {
        return false;
    }
}

// MAKE A TABLE OF BOOKS
const makeTable = function () {
    let response = JSON.parse(this.responseText);

    var getOnLoan = function(bookID){
        idList = findLoanStatus();
    };
    
    var txt = "";
    txt += "<table><tr><th>ID</th><th>Title</th><th>Publisher</th><th>Loan Status</th><th>See Loan Details</th><th>Delete book?</th></tr>"
    for (x in response) {
        let book_publisher = response[x].name;
        for (y in response[x].Books) {
            txt += "<tr><td>" + response[x].Books[y].id + "</td><td>" + response[x].Books[y].title + "</td><td>" + book_publisher + "</td><td>" + getLoans(response[x].Books[y].id) + "</td><td><input type='button' onclick='makeLoanRequest(" + response[x].Books[y].id + ")' value='Details'></td><td><input type='button' onclick='deleteButton(" + response[x].Books[y].id + ")' value='Delete'></td></tr>";
        };    
    };
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

//SEARCH FOR A BOOK
const makeAPIQuery = function(search_term) {
    let rootURL = "http://127.0.0.1:3000/search";
    
    var params = {
        name: search_term
    }

    let queryURL = rootURL + "?type=publisherbooks&" + encodeParameters(params);

    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", makeTable);
    xhttp.open("GET", queryURL);
    xhttp.send();
};

// SEARCH BUTTON
let submitButton = document.getElementById("search_by_publisher_button");
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


getLoanList();
