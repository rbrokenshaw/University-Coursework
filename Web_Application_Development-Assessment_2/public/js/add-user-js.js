// ADD THE USER TO THE DATABASE
const addUser = function(name,barcode,memberType) {
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "http://127.0.0.1:3000/users");
    xhttp.setRequestHeader('Content-Type', 'application/json');

    var params = {
        name: name,
        barcode: barcode,
        memberType: memberType
    };
    
    xhttp.send(JSON.stringify(params));

    output.innerHTML = "New user sucessfully added: " + name + ". <a href='/add-user'>Click here</a> to add another user.";
}

// CHECK THAT THE BARCODE ISN'T ALREADY IN USE, AND THE INPUT FIELDS ARE NOT EMPTY
const checkUser = function() {
    let response = JSON.parse(this.response);

    let allUsersBarcodes = [];

    for (x in response) {
        allUsersBarcodes.push(response[x].barcode);
    }

    let name = document.getElementById("name").value;
    let barcode = document.getElementById("barcode").value;
    let memberType = document.getElementById("memberType").value;

    for (var i=0; i < allUsersBarcodes.length; i++) {
        if (barcode === allUsersBarcodes[i]) {
            alert("That barcode is already in use");
            return false;
        }
    }

    if (name == "") {
        alert("Please enter a name.");
        return false;
    };

    var checkNum = parseInt(barcode, 10);

    if (! Number.isInteger(checkNum) || barcode.length != 6) {
        alert("Please enter a valid barcode.");
        return false;
    };

    addUser(name,barcode,memberType);
};

// SUBMIT BUTTON
document.querySelector('#user_submit').addEventListener('click', function(){

    var xhttpCheck = new XMLHttpRequest();
    xhttpCheck.open("GET", "http://127.0.0.1:3000/users");
    xhttpCheck.addEventListener("load", checkUser);
    xhttpCheck.send();

});





