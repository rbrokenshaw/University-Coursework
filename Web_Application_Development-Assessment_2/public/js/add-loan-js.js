var booksOnLoan = [];

//MAKE A LIST OF THE BOOKS ALREADY ON LOAN
const fillBookList = function() {
	let response = JSON.parse(this.response);

	for (x in response) {
		booksOnLoan.push(response[x].BookId);
	}
}

//FIND THE BOOKS ALREADY ON LOAN
const findLoans = function() {
	var xhttp2 = new XMLHttpRequest;

	xhttp2.addEventListener("load", fillBookList);
    xhttp2.open("GET", "http://127.0.0.1:3000/loans");
    xhttp2.send();
}

findLoans();

// MAKE A SEARCH STRING
const encodeParameters = function(params) {
    var strArray = [];
    Object.keys(params).forEach(function(key) {
        var paramString = encodeURIComponent(key) + "=" + encodeURIComponent(params[key]);
        strArray.push(paramString);
    });
    return strArray.join("&");
};

//GET THE ID OF THE BOOK TO BE BORROWED, CHECK IT ISN'T ALREADY ON LOAN AND ASK FOR A DUE DATE
const addLoan = function(getID,chosenUser){
	var submitLoan = function() {
		let book_id = enterABook.value;
		let user_id = getID

		var bookArrayLength = booksOnLoan.length;
		for (var i = 0; i < bookArrayLength; i++) {
		    if (booksOnLoan[i] == book_id) {
		    	alert("Sorry, that book is already out on loan.")
		    	return false;
		    }
		}

		var checkID = parseInt(book_id, 10);

		if (! Number.isInteger(checkID) || book_id.length == 0) {
		    alert("Please enter a valid book ID.");
		    return false;
    	};

		//CREATE A DROPDOWN LIST FOR DATE - WARNING: LOTS OF TEXT!
		var chooseDateP = document.createElement("P");
		var chooseDatePText = document.createTextNode("Please enter the due date (YYYY/MM/DD):");
		chooseDateP.appendChild(chooseDatePText);

		// YEAR
		var dateYearDropdown = document.createElement("SELECT");
		var yearOption2019 = document.createElement("OPTION");
		var yearOption2020 = document.createElement("OPTION");
		yearOption2019.text = "2019";
		yearOption2020.text = "2020";
		dateYearDropdown.add(yearOption2019);
		dateYearDropdown.add(yearOption2020);

		//MONTH
		var dateMonthDropdown = document.createElement("SELECT");
		var monthOptionJan = document.createElement("OPTION");
		var monthOptionFeb = document.createElement("OPTION");
		var monthOptionMar = document.createElement("OPTION");
		var monthOptionApr = document.createElement("OPTION");
		var monthOptionMay = document.createElement("OPTION");
		var monthOptionJun = document.createElement("OPTION");
		var monthOptionJul = document.createElement("OPTION");
		var monthOptionAug = document.createElement("OPTION");
		var monthOptionSep = document.createElement("OPTION");
		var monthOptionOct = document.createElement("OPTION");
		var monthOptionNov = document.createElement("OPTION");
		var monthOptionDec = document.createElement("OPTION");

		monthOptionJan.text = "01";
		monthOptionFeb.text = "02";
		monthOptionMar.text = "03";
		monthOptionApr.text = "04";
		monthOptionMay.text = "05";
		monthOptionJun.text = "06";
		monthOptionJul.text = "07";
		monthOptionAug.text = "08";
		monthOptionSep.text = "09";
		monthOptionOct.text = "10";
		monthOptionNov.text = "11";
		monthOptionDec.text = "12";

		dateMonthDropdown.add(monthOptionJan);
		dateMonthDropdown.add(monthOptionFeb);
		dateMonthDropdown.add(monthOptionMar);
		dateMonthDropdown.add(monthOptionApr);
		dateMonthDropdown.add(monthOptionMay);
		dateMonthDropdown.add(monthOptionJun);
		dateMonthDropdown.add(monthOptionJul);
		dateMonthDropdown.add(monthOptionAug);
		dateMonthDropdown.add(monthOptionSep);
		dateMonthDropdown.add(monthOptionOct);
		dateMonthDropdown.add(monthOptionNov);
		dateMonthDropdown.add(monthOptionDec);

		//DAY
		var dateDayDropdown = document.createElement("SELECT");
		var dayOption01 = document.createElement("OPTION");
		var dayOption02 = document.createElement("OPTION");
		var dayOption03 = document.createElement("OPTION");
		var dayOption04 = document.createElement("OPTION");
		var dayOption05 = document.createElement("OPTION");
		var dayOption06 = document.createElement("OPTION");
		var dayOption07 = document.createElement("OPTION");
		var dayOption08 = document.createElement("OPTION");
		var dayOption09 = document.createElement("OPTION");
		var dayOption10 = document.createElement("OPTION");
		var dayOption11 = document.createElement("OPTION");
		var dayOption12 = document.createElement("OPTION");
		var dayOption13 = document.createElement("OPTION");
		var dayOption14 = document.createElement("OPTION");
		var dayOption15 = document.createElement("OPTION");
		var dayOption16 = document.createElement("OPTION");
		var dayOption17 = document.createElement("OPTION");
		var dayOption18 = document.createElement("OPTION");
		var dayOption19 = document.createElement("OPTION");
		var dayOption20 = document.createElement("OPTION");
		var dayOption21 = document.createElement("OPTION");
		var dayOption22 = document.createElement("OPTION");
		var dayOption23 = document.createElement("OPTION");
		var dayOption24 = document.createElement("OPTION");
		var dayOption25 = document.createElement("OPTION");
		var dayOption26 = document.createElement("OPTION");
		var dayOption27 = document.createElement("OPTION");
		var dayOption28 = document.createElement("OPTION");
		var dayOption29 = document.createElement("OPTION");
		var dayOption30 = document.createElement("OPTION");
		var dayOption31 = document.createElement("OPTION");

		dayOption01.text = "01";
		dayOption02.text = "02";
		dayOption03.text = "03";
		dayOption04.text = "04";
		dayOption05.text = "05";
		dayOption06.text = "06";
		dayOption07.text = "07";
		dayOption08.text = "08";
		dayOption09.text = "09";
		dayOption10.text = "10";
		dayOption11.text = "11";
		dayOption12.text = "12";
		dayOption13.text = "13";
		dayOption14.text = "14";
		dayOption15.text = "15";
		dayOption16.text = "16";
		dayOption17.text = "17";
		dayOption18.text = "18";
		dayOption19.text = "19";
		dayOption20.text = "20";
		dayOption21.text = "21";
		dayOption22.text = "22";
		dayOption23.text = "23";
		dayOption24.text = "24";
		dayOption25.text = "25";
		dayOption26.text = "26";
		dayOption27.text = "27";
		dayOption28.text = "28";
		dayOption29.text = "29";
		dayOption30.text = "30";
		dayOption31.text = "31";

		dateDayDropdown.add(dayOption01);
		dateDayDropdown.add(dayOption02);
		dateDayDropdown.add(dayOption03);
		dateDayDropdown.add(dayOption04);
		dateDayDropdown.add(dayOption05);
		dateDayDropdown.add(dayOption06);
		dateDayDropdown.add(dayOption07);
		dateDayDropdown.add(dayOption08);
		dateDayDropdown.add(dayOption09);
		dateDayDropdown.add(dayOption10);
		dateDayDropdown.add(dayOption11);
		dateDayDropdown.add(dayOption12);
		dateDayDropdown.add(dayOption13);
		dateDayDropdown.add(dayOption14);
		dateDayDropdown.add(dayOption15);
		dateDayDropdown.add(dayOption16);
		dateDayDropdown.add(dayOption17);
		dateDayDropdown.add(dayOption18);
		dateDayDropdown.add(dayOption19);
		dateDayDropdown.add(dayOption20);
		dateDayDropdown.add(dayOption21);
		dateDayDropdown.add(dayOption22);
		dateDayDropdown.add(dayOption23);
		dateDayDropdown.add(dayOption24);
		dateDayDropdown.add(dayOption25);
		dateDayDropdown.add(dayOption26);
		dateDayDropdown.add(dayOption27);
		dateDayDropdown.add(dayOption28);
		dateDayDropdown.add(dayOption29);
		dateDayDropdown.add(dayOption30);
		dateDayDropdown.add(dayOption31);

		dateSubmit = document.createElement("BUTTON");
		dateSubmitText = document.createTextNode("Confirm Date");
		dateSubmit.appendChild(dateSubmitText)

		let outputDiv = document.getElementById("output3")
		outputDiv.appendChild(chooseDateP);
		outputDiv.appendChild(dateYearDropdown);
		outputDiv.appendChild(dateMonthDropdown);
		outputDiv.appendChild(dateDayDropdown);
		outputDiv.appendChild(dateSubmit);
		
		dateSubmit.addEventListener("click", function(){
			let chosenYear = dateYearDropdown.value;
			let chosenMonth = dateMonthDropdown.value;
			let chosenDay = dateDayDropdown.value;

			var dateString = chosenYear + "-" + chosenMonth + "-" + chosenDay;
			var url = "http://127.0.0.1:3000/users/" + user_id + "/loans/" + book_id;

			var xhttp = new XMLHttpRequest();
			xhttp.open("POST", url);
    		xhttp.setRequestHeader('Content-Type', 'application/json');

		    var params = {
		        dueDate: dateString
		    };

		    xhttp.send(JSON.stringify(params));

		    xhttp.onload = function() {
		    	output3.innerHTML = "Book with ID: " + book_id + " has been sucessfully loaned to user " + chosenUser + ".";
			};

		})
	}

	//Prompt the user to input the ID of the book being borrowed
	let inputBookP = document.createElement('P');
	let inputBookPText = document.createTextNode("Please input the ID of the book you wish to loan to " + chosenUser + ":");
	inputBookP.appendChild(inputBookPText);

	let enterABook = document.createElement('INPUT');
	let submitButton = document.createElement('BUTTON');
	let submitButtonText = document.createTextNode("Submit");
	submitButton.appendChild(submitButtonText);

	let outputDiv = document.getElementById("output2");
	outputDiv.appendChild(inputBookP);
	outputDiv.appendChild(enterABook);
	outputDiv.appendChild(submitButton);
	
	submitButton.addEventListener("click", submitLoan);
}

// GET THE SELECTED USER'S ID
const getId = function(chosenUser) {
	chosenUser = String(chosenUser);

	var myRe = new RegExp(/\d{1,}/);
	var getID = myRe.exec(chosenUser);

	addLoan(getID[0],chosenUser)
}

// MAKE A DROPDOWN LIST OF SEARCH RESULTS
const makeDropdown = function() {
	let response = JSON.parse(this.response);

	var txt = "";
	txt += "<select id='chooseUser'>";
	for (x in response) {
		txt += "<option>" + response[x].id + " - " + response[x].name + " - " + response[x].barcode;
	}
	txt += "</select>";

	//submit button for confirming user
	var updateSubmit = document.createElement("BUTTON");
	var submitText = document.createTextNode("Confirm User");
	updateSubmit.appendChild(submitText);

	var outputDiv = document.getElementById("output");
	outputDiv.innerHTML = txt;
	outputDiv.appendChild(updateSubmit);

	updateSubmit.addEventListener("click", function(){
		let chosenUser = document.getElementById("chooseUser").value;
		getId(chosenUser);
	});
}

// SEARCH FOR A USER
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
    xhttp.addEventListener("load", makeDropdown);
    xhttp.open("GET", queryURL);
    xhttp.send();
};

// SEARCH BUTTON
let submitButton = document.getElementById("add_loan_button");
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

