//ADD AUTHOR TO SPECIFIED BOOK
const addAuthor = function(book_id,author_name) {
    let xhttp = new XMLHttpRequest();

    let url = "http://127.0.0.1:3000/books/" + book_id + "/authors/"
    xhttp.open("POST", url);
    xhttp.setRequestHeader('Content-Type', 'application/json');

    var params = {
        name: author_name
    };
    
    xhttp.send(JSON.stringify(params));

    loan_output.innerHTML = "Author " + author_name + " successfully added to book with ID " + book_id;
};

// SUBMIT BUTTON
let submitButton = document.getElementById("author_submit");
submitButton.addEventListener("click", function() {
	let book_id = document.getElementById("book_id").value;
	let author_name = document.getElementById("author_name").value;

    if (book_id == "") {
        alert("Please enter a book ID");
        return false;
    };

    if (author_name == "") {
        alert("Please enter an author.");
        return false;
    };

    addAuthor(book_id,author_name);
});
