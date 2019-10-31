'use static'

const Client = require('../models/client')
const service = require('../services')
const bcrypt = require('bcrypt')

function registerClient(req, res){
    const client = new Client({
        clientId : req.body.clientid,
        password: req.body.password,
        scopes: req.body.scopes
    })
    Client.findOne({clientId: req.body.clientid}, (err,clientFound)=>{
        if(err) return res.status(500).send({estado: '500', mensaje: `Error al crear el cliente: ${err}`})
        if(clientFound) return res.status(409).send({estado: '409', mensaje: `Ya existe un cliente registrado con el mismo Id ${client.clientId}`})
            
        client.save((err)=>{
            if(err) return res.status(500).send({estado: '500', mensaje: `Error al crear el cliente: ${err}`})
            return res.status(200).send({estado: '200', mensaje: `Cliente registrado : ${client.clientId}`})
        })
    })
}

function validateClient(req, res){
    Client.findOne({clientId: req.body.clientid}, (err,client)=>{
        if(err) return res.status(500).send({estado: '500', mensaje: `Ha ocurrido un error al buscar al cliente: ${err}`})
        if(!client)return res.status(404).send({estado: '404', mensaje: 'No existe el cliente registrado'})
        bcrypt.compare(req.body.password, client.password, (err,same)=>{
            if(err) return res.status(500).send({estado: '500', mensaje: `Ha ocurrido un error al comparar contraseñas: ${err}`})
            if(same){
                req.client = client
                res.status(200).send({
                    estado: '200',
                    mensaje: 'Usuario logueado correctamente',
                    data: {
                        token: service.createToken(client)
                    }
                })
            }
            else res.status(401).send({message: 'Credenciales incorrectas'})
        })
    })
}

module.exports = {
    registerClient,
    validateClient
}