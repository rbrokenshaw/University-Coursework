const redirect = function() {
    window.location.href = "/index";
}

const checkLogin = function() {
    let response = JSON.parse(this.response);

    let inputUsername = document.getElementById("username").value;
    let inputPassword = document.getElementById("password").value;

    let outputDiv = document.getElementById("output");

    for (x in response) {
        if (response[x].username === inputUsername && response[x].password === inputPassword) {

            let successP = document.createElement("P");
            let successPText = document.createTextNode("Login successful, redirecting you...");
            successP.appendChild(successPText);
            outputDiv.appendChild(successP);
            window.setTimeout(redirect, 3000);
        } else {
            let failureP = document.createElement("P");
            let failurePText = document.createTextNode("Sorry, login failed. Please check your details and try again.");
            failureP.appendChild(failurePText);
            outputDiv.appendChild(failureP);
        };
    };
};

const getLoginDetails = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:3000/login");
    xhttp.addEventListener("load", checkLogin);
    xhttp.send();
};

let submitButton = document.getElementById("login_submit");
submitButton.addEventListener("click", function() {
    getLoginDetails();
})