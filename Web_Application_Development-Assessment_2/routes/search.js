const express = require("express");
const router = express.Router();
const Sequelize = require("sequelize");
const Op = Sequelize.Op;

const db = require("../data");
const ret = require("../lib/return");

function getSearchParams(queryParams, modelFields) {
    let searchParams = {};
    modelFields.forEach(function(p) {
        p = p.toLowerCase();
        if (queryParams[p]) {
            searchParams[p] = {
                [Op.like]: "%" + queryParams[p] + "%"
            };
        }
    });
    console.log(searchParams);
    return searchParams;
}

function findAll(model, params, res) {
    model.findAll({ where: params }).then(function(results) {
        if (results) {
            ret.json(results, res);
            res.end();
        }
    });
}

function findAllAuthorBooks(model, params, res) {
    model.findAll({
        where: params,
        include: [{
            model: db.Book,
            as: 'Books'
        }]
    }).then(function(results) {
        if (results) {
            ret.json(results, res);
            res.end();
        } 
    })
}

function findAllPublisherBooks(model, params, res) {
    model.findAll({
        where: params,
        include: [{
            model: db.Book,
            as: 'Books'
        }]
    }).then(function(results) {
        if (results) {
            ret.json(results, res);
            res.end();
        } 
    })
}

router.get("/", function(req, res) {
    if (req.query.type.toLowerCase() === "book") {
        findAll(db.Book, getSearchParams(req.query, ["title", "isbn"]), res);
    } else if (req.query.type.toLowerCase() === "authorbooks") {
        findAllAuthorBooks(db.Author, getSearchParams(req.query, ["name"]), res);
    } else if (req.query.type.toLowerCase() === "publisherbooks") {
        findAllPublisherBooks(db.Publisher, getSearchParams(req.query, ["name"]), res);
    } else if (req.query.type.toLowerCase() ===  "author") {
        findAll(db.Author, getSearchParams(req.query, ["name"]), res);
    } else if (req.query.type.toLowerCase() === "user") {
        findAll(db.User, getSearchParams(req.query, ["name", "barcode", "memberType"]), res);
    } else {
        res.end();
    }
});

module.exports = router;
