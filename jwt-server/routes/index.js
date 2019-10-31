'use strict'

const express = require('express')
const api = express.Router()
const clientCtrl = require('../controllers/client')

api.post('/post/autorizacion', clientCtrl.validateClient)
api.post('/client', clientCtrl.registerClient)

module.exports = api