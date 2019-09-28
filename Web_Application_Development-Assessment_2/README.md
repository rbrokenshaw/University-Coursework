Coursework 2 - Interactive Website Development

Assignment Instructions:

PontyBridge University are back. They’re so impressed with the work you did on their
prototype website in the first assignment that they’ve returned to the company with
another project and specifically requested you work on it.

The University has bought a new backend for their Library system. This is a simple server
application that allows the University to track the books that they have, the library users, 
and which users have borrowed which books. Unfortunately, they forgot to buy a front-end
for the system, so they need you to write one.

The code for the Library server is available at git@gitlab.cs.cf.ac.uk:somerepo. You should
download the code and familiarise yourself with it. Full usage instructions are included in
the Readme.md file contained in the project repository.

The applications itself provides a simple server with a REST API which has the following
functionality:
• API endpoints:
/users
/books
/loans

Each API endpoint accepts HTTP requests with the verbs GET, POST, PUT and DELETE.
The application also comes with an .sqlite database in which the data for the application is
stored, and an ORM mapping between the database objects and JavaScript objects. Further
documentation on the API server is available in the Library system source code and through
the provided tests.

You are tasked with creating a front-end website that interfaces with this API to provide the
library functionality requested by the University. This system will be used by the librarians
to manage their library and associated data. Your front end should allow them to:
U1 - Add a new User to the Library system with the fields Name, Barcode and Member Type
(Staff/Student).
U2 - Get a User’s details from the Library system by searching on Name or Barcode
U3 - Update a User’s Name or Member Type
U4 - Remove a User
B1 - Add a new Book to the Library system with the fields Title, ISBN, Authors.
B2 - Get a Book’s details by searching on Title or Author
B3 - Remove a Book
L1 - Loan a Book to a User (if it is not already out on Loan), specifying the Due Date
L2 - Get a list of a User’s current Loans
L3 - Get the User currently borrowing a Book

API endpoints are implemented in the Server application to allow this functionality,
documentation comments on each endpoint and the parameters accepted are included in
the server application source code.

You are free to modify the server code as you see fit. You are also free to add additional
functionality beyond that requested by the University. Alongside the final source code for
your front-end (and the server application if you have modified that) you should submit a
short document describing the functionality you have implemented. This does not need to 
be extensive: one or two sentences on each functional requirement, indicating how and
where you have implemented the functionality is fine. You may also include screenshots
showing the website functionality.

# CMT112-CW2-Library Server

## Installation

Download and install all requirements for the server with:

```
npm install
```

## Initialising a Database

Before you run the server for the first time, you should ensure there is a database available for it to read and write to. You can initialise the database with:

```
node initialise_database.js
```

This will create a `library.sqlite` file inside the `data/` directory and pre-populate it with some sample data.

**CAUTION!** Running this command will remove any data already stored in the database `data/library.sqlite`. It should be used with caution, only when you want to reset the Database to its initial state.

## Running the Server

Start the server with:

```
node server.js
```

This will start the server running on `127.0.0.1` port `3000`.

## Check everything is working correctly

To check the database and server are operating correctly you can open `http://127.0.0.1:3000/authors` in a Web Browser. This should return a JSON representation of all the Authors stored in the database.

## Making requests

Requests to the server can be made to the endpoints specified in `server.js`. For details on the Models and the Fields they contain, check `data.js`

### `authors/...`

**GET /**

Returns a list of all Authors in the database. If requested with the parameter `allEntities`, Author objects returned will include full details of all Books authored by each Author, otherwise only `bookID`s will be provided

Accepted query parameters: `allEntities`

```
GET http://127.0.0.1/authors
GET http://127.0.0.1/authors?allEntities=true
```

**GET /:authorID**

Returns the Author with the specified `authorID`. If requested with the parameter `allEntities`, Author object returned will include full details of all Books authored by this Author, otherwise only `bookID`s will be provided

Accepted query parameters: `allEntities`

```
GET http://127.0.0.1/authors/1
GET http://127.0.0.1/authors/1?allEntities=true
```

**PUT /:authorID**

Updates the Author with the specified `authorID`. Fields to be updated should be included as the body of the PUT request.

Accepted body fields: `name`

```
PUT http://127.0.0.1/authors/1
{"name" : "Dave"}
```

**DELETE /:authorID**

Deletes the Author with the specified `authorID`

```
DELETE http://127.0.0.1/authors/1
```

**POST /**

Creates a new Author. Fields for the Author should be included as the body of the POST request

Accepted body fields: `name`

```
POST http://127.0.0.1/authors
{"name" : "Dave"}
```

**POST /:authorID/books**

Adds a Book to the list of books written by the Author with the specified `authorID`. Will create the Book if a Book with matching details is not found. Fields for the Book should be included in the body of the POST request

Accepted body fields: `bookTitle`, `bookISBN`

```
POST http://127.0.0.1/authors/1/books
{
    "bookTitle": "Building Library Systems",
    "bookISBN": "3985789305"
}
```

**POST /:authorID/books/:bookID**

Adds the Book with the specified `bookID` to the list of books written by the Author with the specified `authorID`

```
POST http://127.0.0.1/authors/1/books/1
```

### `books/...`

**GET /**

Returns a list of all Books in the database. If requested with the parameter `allEntities`, Book objects returned will include full details of all Authors of each Book, otherwise only `authorID`s will be provided

Accepted query parameters: `allEntities`

```
GET http://127.0.0.1/books
GET http://127.0.0.1/books?allEntities=true
```

**GET /:bookID**

Returns the Book with the specified `bookID`. If requested with the parameter `allEntities`, Book objects returned will include full details of all Authors of this Book, otherwise only `authorID`s will be provided

Accepted query parameters: `allEntities`

```
GET http://127.0.0.1/books/1
GET http://127.0.0.1/books/1?allEntities=true
```

**PUT /:bookID**

Updates the Book with the specified `bookID`. Fields to be updated should be included as the body of the PUT request.

Accepted fields: `title`, `isbn`

```
PUT http://127.0.0.1/books/1
{
    "title": "Building Library Systems",
    "isbn": "3985789305"
}
```

**DELETE /:bookID**

Deletes the Book with the specified `bookID`

```
DELETE http://127.0.0.1/books/1
```

**POST /**

Creates a new Book. Fields for the Book should be included as the body of the POST request

Accepted fields: `title`, `isbn`

```
POST http://127.0.0.1/books
{
    "title": "Building Library Systems",
    "isbn": "3985789305"
}
```

**POST /:bookID/authors**

Adds an Author to the list of authors for the Book with the specified `bookID`. Will create the Author if an Author with matching details is not found. Fields for the Author should be included in the body of the POST request

Accepted fields: `name`

```
POST http://127.0.0.1/books/1/authors
{"name": "David"}
```

**POST /:bookID/authors/:authorID**

Adds the Author with the specified `auhtorID` to the list of authors of the Book with the specified `bookID`

```
POST http://127.0.0.1/books/1/authors/2
```

### `users/...`

**GET /**

Returns a list of all Users in the database

```
GET http://127.0.0.1/users
```

**GET /:userID**

Returns the User with the specified `userID`

```
GET http://127.0.0.1/users/1
```

**POST /**

Creates a new User. Fields for the new User should be included in the body of the POST request.

Accepted body fields: `name`, `barcode`, `memberType`

```
POST http://127.0.0.1/users
{
    "name": "Sarah",
    "barcode": "39587985",
    "memberType": "Student"
}
```

**PUT /:userID**

Updates the details of the User with the specified `userID`. Fields to be updated should be included in the body of the PUT request

Accepted body fields: `name`, `barcode`, `memberType`

```
PUT http://127.0.0.1/users/1
{
    "name": "Sarah",
    "barcode": "39587985",
    "memberType": "Student"
}
```

**DELETE /:userID**

Deletes the User with the specified `userID`.

```
DELETE http://127.0.0.1/users/1
```

**GET /:userID/loans**

Returns the list of Loans for the User with the specified `userID`.

```
POST http://127.0.0.1/users/1/loans
```

**POST /:userID/loans/:bookID**

Creates or Updates a Loan for the User with the specified `userID` and the Book with the specified `bookID`. Fields to be added to or updated in the Loan should be included in the body of the POST request

Accepted body fields: `dueDate`

```
POST http://127.0.0.1/users/1/loans/2
{"dueDate": "2018-12-31"}
```

### `loans/...`

**GET /**

Returns a list of all Loans in the Database

```
GET http://127.0.0.1/loans
```

**GET /:loanID**

Returns the details of the Loan with the specified `loanID`

```
GET http://127.0.0.1/loans/1
```

**PUT /:loanID**

Updates the details of the Loan with the specified `loanID`. Fields to be updated should be included in the body of the PUT request

Accepted body fields: `dueDate`

```
GET http://127.0.0.1/loans/1
{"dueDate": "2018-12-31"}
```

**DELETE /:loanID**

Deletes the Loan with the specified `loanID`

```
DELETE http://127.0.0.1/loans/1
```

### `/search`

**GET /**

Searches for a particular item in the database. Parameters are used to control what type of item being searched for and to supply fields to match.

Parameters accepted: `type` + [`title`, `isbn`] + [`name`] + [`name`, `barcode`, `memberType`]

```
GET http://127.0.0.1/search?type=book&title=javascript
GET http://127.0.0.1/search?type=author&name=david
GET http://127.0.0.1/search?type=user&barcode=3265897236
```

## Editing the server

The Node server uses the [Sequelize](http://docs.sequelizejs.com/) library for interacting with the SQLite database.

It uses the [Express](https://expressjs.com/) framework for running the web server and routing queries.

## Server Test Page

This repository also contains a server test page - `server_test.html`. This can be used both to check the server is operating correctly and to act as an example of how to make requests to the server.

