// Source for reference: http://docs.sequelizejs.com/

const express = require("express");
const router = express.Router();

const db = require("../data");
const ret = require("../lib/return");

router.get("/", function(req, res) {
    db.Administrator.findAll().then(function(admins) {
        ret.json(admins, res);
    });
});

module.exports = router;
