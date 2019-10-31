'use strict'

const mongoose = require('mongoose')
const Schema = mongoose.Schema
const bcrypt = require('bcrypt')

mongoose.set('useCreateIndex', true)

const ClientSchema = new Schema({
    clientId : { type: String, unique: true, lowercase: true },
    password : String,
    scopes : [String]
})

ClientSchema.pre('save', function(next){
    let client = this
    if(!client.isModified('password')) return next()

    bcrypt.genSalt(10, function(err, salt){
        if(err) return next(err)

        bcrypt.hash(client.password, salt, function(err, hash){
            if(err)return next(err)

            client.password = hash
            next()
        })
    })
})


module.exports = mongoose.model('Client', ClientSchema)