'use strict'

const mongoose = require('mongoose')
const app = require('./app')
const config = require('./config')

mongoose.set('useNewUrlParser', true);
mongoose.set('useUnifiedTopology', true);

mongoose.connect(config.db, (err,res)=>{
    if(err) {
        return console.log(`Error en la conexión a la BD: ${err}`)
    }
    console.log('Conexión BD establecida'); 

    app.listen(config.port, ()=>{
        console.log(`API rest running in http://localhost: ${config.port}`)
    })

})