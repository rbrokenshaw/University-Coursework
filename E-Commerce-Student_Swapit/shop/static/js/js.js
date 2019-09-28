let the_search_term = ""

const submitSell = function(title, isbn, publishers, authors, condition, price, category, cover) {
    document.getElementById("form-isbn").value = isbn;
    document.getElementById("form-title").value = title;
    document.getElementById("form-authors").value = authors;

    if (category.length == 0) {
        var firstcategory = "";
    } else {
        var firstcategory = category[0];
    }

    document.getElementById("form-category").value = firstcategory;
    document.getElementById("form-publishers").value = publishers;
    document.getElementById("form-cover").value = cover;
}

const processResponse = function() {
    let response = JSON.parse(this.response);
    if (Object.entries(response).length === 0 && response.constructor === Object) {
        let nomatches = document.createElement("p");
        let nomatchestext = document.createTextNode("Sorry, we couldn't find any matches for that ISBN. Please manually input the book's information below:")
        nomatches.appendChild(nomatchestext);

        let outputdiv = document.getElementById("selloutput")

        let cover = "/static/img/books/default.jpg";
        document.getElementById("form-cover").value = cover;

        outputdiv.appendChild(nomatches);
    } else {
        let isbnString = "ISBN:" + the_search_term;
        let isbn = the_search_term;
        let title = "";
        let authors = [];
        let publishers = [];
        let cover = "";
        let categories = [];
        let condition = "";
        let price = "";

        if (response[isbnString].title) {
            title = response[isbnString].title;
        };

        if (response[isbnString].authors) {
            for (i = 0; i < response[isbnString].authors.length; i++ ) {
                authors.push(response[isbnString].authors[i].name);
            };
        };

        if (response[isbnString].publishers) {
            for (i = 0; i < response[isbnString].publishers.length; i++){
                publishers.push(response[isbnString].publishers[i].name);
            };
        };

        if (response[isbnString].subjects) {
            for (i = 0; i < response[isbnString].subjects.length; i++) {
                if (response[isbnString].subjects[i].name != "In library") {
                    categories.push(response[isbnString].subjects[i].name)
                };
            };
        }

        let outputdiv = document.getElementById("selloutput");

        // Cover image output
        let defaultcover = "/static/img/books/default.jpg";

        if (response[isbnString].cover) {
            cover = response[isbnString].cover.medium;
        };

        if (cover != "") {
            let coverimg = document.createElement("IMG");
            coverimg.src = cover;

            outputdiv.appendChild(coverimg);
        } else {
            let coverimg = document.createElement("IMG");
            coverimg.src = defaultcover;
            cover =defaultcover;

            outputdiv.appendChild(coverimg);
        }

        submitSell(title, isbn, publishers, authors, condition, price, categories, cover);
    };
};

const makeAPIQuery = function(search_term) {
    let rootURL = "https://openlibrary.org/api/books?bibkeys=ISBN:";
    let URLend = "&jscmd=data&format=json";

    search_term = search_term.replace('-', '')

    let queryURL = rootURL + search_term + URLend;

    the_search_term = search_term;

    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", processResponse);
    xhttp.open("GET", queryURL);
    xhttp.send();
};