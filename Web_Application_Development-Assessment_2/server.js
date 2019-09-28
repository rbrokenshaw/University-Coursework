const createError = require("http-errors");
const express = require("express");
const cors = require("cors");
const db = require("./data");

let authorsRouter = require("./routes/authors");
let booksRouter = require("./routes/books");
let usersRouter = require("./routes/users");
let loansRouter = require("./routes/loans");
let searchRouter = require("./routes/search");

let server = express();

// CHANGES START HERE

// Login router added
let loginRouter = require("./routes/login");

// Templating with ejs tutorial https://scotch.io/tutorials/use-ejs-to-template-your-node-application (accessed 17/01/2019)
// set the view engine to ejs
server.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// login page 
server.get('/', function(req, res) {
    res.render('pages/login');
});

// login page 
server.get('/index', function(req, res) {
    res.render('pages/index');
});

// all books page
server.get('/all-books', function(req, res) {
    res.render('pages/all-books');
});

// search books by title/isbn page
server.get('/search-books', function(req, res) {
    res.render('pages/search-books');
});

// search books by author page
server.get('/search-books-by-author', function(req, res) {
    res.render('pages/search-books-by-author');
});

// search books by author page
server.get('/search-books-by-publisher', function(req, res) {
    res.render('pages/search-books-by-publisher');
});

// add a book page
server.get('/add-book', function(req, res) {
    res.render('pages/add-book');
});

// add an author to a book page
server.get('/add-author', function(req, res) {
    res.render('pages/add-author');
});

// add a loan page
server.get('/add-loan', function(req, res) {
    res.render('pages/add-loan');
});

// view user loans page
server.get('/view-user-loans', function(req, res) {
    res.render('pages/view-user-loans');
});

// all users page
server.get('/all-users', function(req, res) {
    res.render('pages/all-users');
});

// search users page
server.get('/search-users', function(req, res) {
    res.render('pages/search-users');
});

// add user page
server.get('/add-user', function(req, res) {
    res.render('pages/add-user');
});

server.use(express.static(__dirname + '/public'));

//CHANGES END HERE

// interpret JSON body of requests
server.use(express.json());

// interpret url-encoded queries
server.use(express.urlencoded({ extended: false }));

// allow CORS
server.use(cors());

// allow CORS preflight for all routes
server.options("*", cors());

server.use("/authors", authorsRouter);
server.use("/books", booksRouter);
server.use("/users", usersRouter);
server.use("/loans", loansRouter);
server.use("/search", searchRouter);

// ADDED
server.use("/login", loginRouter);

// handle errors last
server.use(function(err, req, res, next) {
    res.status = err.status || 500;
    res.send(err);
});

// connect to the database and start the server running
db.initialiseDatabase(false, null);
server.listen(3000, function() {
    console.log("server listening");
});
