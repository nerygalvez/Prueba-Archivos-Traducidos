'use strict'

const jwt = require('jwt-simple')
const moment = require('moment')
const config = require('../config')

function createToken(client){
    const payload = {
        auth: 'true',
        exp: moment().add(2, 'minutes').unix(),
        clientid: client.clientId,
        scopes: client.scopes
    }

    return jwt.encode(payload, config.SECRET, 'RS256')
}

module.exports = {
    createToken
}