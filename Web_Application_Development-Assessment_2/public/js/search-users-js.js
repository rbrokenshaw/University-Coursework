var deleteButton = function(id) {
	let user_id = id;

	if (confirm('Are you sure you want to delete this user? Click "OK" to proceed.')) {
		var user_url = "http://127.0.0.1:3000/users/" + user_id
	    var xhttp = new XMLHttpRequest();

	    xhttp.open("DELETE", user_url);
	    xhttp.send();

	    var outputDiv = document.getElementById("update_output");
	    outputDiv.innerHTML = "User wth id " + user_id + " successfully deleted.";

	    var refreshButton = document.createElement("BUTTON");
    	var refreshButtonText = document.createTextNode("Refresh Results");
    	refreshButton.appendChild(refreshButtonText);
    	let outputDiv2 = document.getElementById("refresh_output")
    	outputDiv2.appendChild(refreshButton);

    	refreshButton.addEventListener("click", function() {
    		let search_term = document.getElementById("search_term").value;

        	makeAPIQuery(search_term);
        });
	} else {
		return false;
	}

};

var updateButton = function(id) {
	let user_id = id;

	// title for updating a user
	var updateP = document.createElement("P");
	var updatePText = document.createTextNode("Update user with ID:" + user_id);
	updateP.appendChild(updatePText);

	// title for name input box
	var nameP = document.createElement("P");
	var nameText = document.createTextNode("Name: ");
	nameP.appendChild(nameText);

	// update name input box
	var updateUserName = document.createElement("INPUT");
	updateUserName.setAttribute("type", "text");

	// title for name input box
	var memberTypeP = document.createElement("P");
	var memberTypeText = document.createTextNode("Member Type:");
	memberTypeP.appendChild(memberTypeText);

	//dropdown box for selecting member type
	var memberTypeDropdown = document.createElement("SELECT");
	var opt1 = document.createElement("OPTION");
	var opt2 = document.createElement("OPTION");
	opt1.text= "Staff";
	opt1.value = "Staff";
	opt2.text = "Student";
	opt2.value = "Student";
	memberTypeDropdown.options.add(opt1);
	memberTypeDropdown.options.add(opt2);

	//submit button for update
	var updateSubmit = document.createElement("BUTTON");
	var submitText = document.createTextNode("Update");
	updateSubmit.appendChild(submitText);


	// output everything to the div
	var outputDiv = document.getElementById("update_output");
	outputDiv.innerHTML = "";
	outputDiv.appendChild(updateP);
	outputDiv.appendChild(nameText);
	outputDiv.appendChild(updateUserName);
	outputDiv.appendChild(memberTypeP);
	outputDiv.appendChild(memberTypeDropdown);
	outputDiv.appendChild(updateSubmit);

	updateSubmit.addEventListener("click", function(){
	    let user_name = updateUserName.value;
	    let user_memberType = memberTypeDropdown.value;

	    var user_url = "http://127.0.0.1:3000/users/" + user_id
	    var xhttp = new XMLHttpRequest();

	    xhttp.open("PUT", user_url);
	    xhttp.setRequestHeader('Content-Type', 'application/json')

	    //If the user inputs a member type only, update the member type only
    	if (user_name == "" && user_memberType != "") {
        	var params = {
            	memberType: user_memberType
        	};
        } else {

	        var params = {
	            name: user_name,
	            memberType: user_memberType
	        };
	    };

	    xhttp.send(JSON.stringify(params));

    	outputDiv.innerHTML = "User with id " + user_id + " successfully updated.";

    	var refreshButton = document.createElement("BUTTON");
    	var refreshButtonText = document.createTextNode("Refresh Results");
    	refreshButton.appendChild(refreshButtonText);
    	let outputDiv2 = document.getElementById("refresh_output")
    	outputDiv2.appendChild(refreshButton);

    	refreshButton.addEventListener("click", function() {
    		let search_term = document.getElementById("search_term").value;

        	makeAPIQuery(search_term);
        });
    });	
};


const makeTable = function() {
	let response = JSON.parse(this.response);

	var txt = "";
	txt += "<table><tr><th>ID</th><th>Name</th><th>Barcode</th><th>Member Type</th><th>Update User?</th><th>Delete User?</th></tr>"
	for (x in response) {
		txt += "<tr><td>" + response[x].id + "</td><td>" + response[x].name + "</td><td>" + response[x].barcode + "</td><td>" + response[x].memberType + "</td><td><input type='button' onclick='updateButton(" + response[x].id + ")' value='Update'></td><td><input type='button' onclick='deleteButton(" + response[x].id + ")' value='Delete'></td></tr>";
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
let submitButton = document.getElementById("search_users_button");
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

