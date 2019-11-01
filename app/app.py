from typing import List, Dict
from flask import Flask,render_template,request,jsonify,redirect, abort, send_from_directory, url_for
import os
import sys
import polib
import time
import requests
import mysql.connector
import json
import jwt

UPLOAD_DIRECTORY = "pfiles/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return redirect('/listarComplementos')


@app.route('/post/complementoTraducido', methods=['POST'])
def ComplementoTraducido():


    solicitud = request.get_json(force=True, silent = True) #Le digo que si hay error al parsear el JSON no muera, sino que retorne None

    #Verifico si se puede parsear el JSON recibido
    if solicitud == None:
        return jsonify(
                    estado='500',
                    mensaje='Existe un error en la estructura del JSON con el que se hace la solicitud /post/complementoTraducido',
                   )
    
    #Si sí se pudo parsear la solicitud a JSON obtengo los datos que se envían
    token = solicitud.get('token') #se verifica primero el token
    
    #validarToken = getValidationToken(token)
    #if not validarToken: #si no retorna True hubo un problema con el token
    #    return validarToken     #retorna un JSON con el error

    nombre_usuario = solicitud.get('nombre') #Nombre de usuario original
    correo_usuario = solicitud.get('correo') #Correo de usuario original
    complemento = solicitud.get('complemento')

    nombre_complemento = complemento['nombre']
    localizacionOriginal = complemento['localizacionOriginal']
    localizacionTraducida = complemento['localizacionTraducida']
    contenido = complemento['contenido']
    contenido_string = json.dumps(contenido)



    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'Traducido',
        #'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    

    cursor.callproc('sp_traducidosubeArchivo', [nombre_usuario,correo_usuario,nombre_complemento,localizacionTraducida,contenido_string, ])

    global resultado

    #results = {"Nombre":"Nery Gonzalo Galvez Gomez"}
    for result in cursor.stored_results():
        resultado = result.fetchall()
     
    
    connection.commit()

    cursor.close()
    connection.close()

    
    return jsonify(
                    estado = resultado[0][0],
                    mensaje = resultado[0][1],
                )
    
    #return render_template('index.html', data=results)


@app.route('/listarComplementos')
def listarComplementos() -> str:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'Traducido',
        'auth_plugin':'mysql_native_password'
    }


    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT idDetalleArchivo, Complemento,Localizacion,nombreusr,correousr FROM ArchivoCadena')
    results = [{"idDetalleArchivo": idDetalleArchivo, "Complemento" : Complemento, "Localizacion" : Localizacion, "nombreusr" : nombreusr, "correousr" : correousr} for (idDetalleArchivo, Complemento,Localizacion,nombreusr,correousr) in cursor]
    cursor.close()
    connection.close()

    return render_template('complementos.html', data=results)


@app.route('/suscripcionAlmacenamiento',methods=['GET'])
def suscripcionAlmacenamiento():
    token = obtenerNuevoToken() #Genero un nuevo token
    #"ip":"127.0.0.1:5003"
    parametros = {"token":token, "ip":os.environ["IP_TRADUCIDOS"] + ':' + os.environ["TRADUCIDOS_PORT"]}
    ruta_solicitud = 'http://' + os.environ["IP_ALMACENAMIENTO"] + ':' + os.environ["ALMACENAMIENTO_PORT"] + '/post/suscripcion'
    response = requests.post(ruta_solicitud, json=parametros)

    #Debería de obtener un json Respuesta
    """
        {
            "codigo":"200",
            "mensaje":"Suscrito correctamente"
        }
    """
    #return response.text
    return redirect('/listarComplementos') #Redirecciono a la lista de complementos


@app.route('/pruebaObtenerToken',methods=['GET'])
def pruebaObtenerToken():
    token = obtenerNuevoToken()

    return jsonify(
                    token = token,
                   )


#Función que solicita un token al servidor JWT
def obtenerNuevoToken():
    #headers = {'your_header_title': 'your_header'}
    # In you case: headers = {'content-type': 'application/json'}
    #r = requests.post("your_url", headers=headers, data=your_data)

    headers = {'Content-Type': 'application/json'}


    parametros = {"clientid":"grupo1", "password":"grupo1"}
    #ruta_solicitud = 'http://' + '35.192.23.213:5004' + '/post/autorizacion'
    ruta_solicitud = 'http://' + os.environ["IP_JWT"] + ':' + os.environ["JWT_PORT"] + '/post/autorizacion'
    response = requests.post(ruta_solicitud, headers=headers, json=parametros)

    respuesta = json.loads(response.text)

    #Verifico si se puede parsear el JSON recibido
    if respuesta == None:
        return jsonify(
                    estado='500',
                    mensaje='Existe un error en la estructura del JSON que devuelve el servidor JWT',
                   )
    
    if respuesta["estado"] == "200": #Si se generó el token correctamente
        data = respuesta["data"]
        token = data["token"]
        return token #Retorno el token generado

    return respuesta #Retorno el json con el código de error y el mensaje


#Función que retorna True si es valido el token sino retorna el error
#el parametro token es la llave privada que envia el microservicio por medio de su payload
#def getValidationToken(token, funcionSolicitada):
def getValidationToken(token):
    if token == None: #que el token no venga null
        return jsonify(
                    estado='500',
                    mensaje='Existe un error en el token enviado viene nulo',
                   )

    try:
        f =open("../publickeys/publickey.ssh","r")
        content = f.read() #os.environ['NODE_PUBLICKEY'] 
        f.close()          
    except FileNotFoundError:
        return jsonify(
            estado='500',
            mensaje='El archivo de la llave publica no existe'
        )

    try:
        decoded = jwt.decode(token, content, algorithms='RS256')
        auth =  decoded["auth"]
        if auth == "true":
            #scopes = decoded["scopes"]
            ##recorrer scopes
            #for x in scopes:
            ##validar que la funcion Solicitada existe el scope
            #    if x == funcionSolicitada or funcionSolicitada == None:
            #        #retornar error si no existe
            #        return True
            return True #el token es correcto
            
            #return jsonify(
            #    estado='500',
            #    mensaje='El scope es inválido.',
            #)        
        return jsonify(
            estado='500',
            mensaje='El token es inválido.',
        )
    except jwt.ExpiredSignatureError:
        #el tiempo ha expirado será comparado con el tiempo actual UTC , timegm(datetime.utcnow().utctimetuple()))
        return jsonify(
                    estado='500',
                    mensaje='El token ha expirado.',
                   )
    except jwt.DecodeError:
        #tira una excepción cuando la validación del token falla
        return jsonify(
                    estado='500',
                    mensaje='La validación del token ha fallado no viene porque el token viene alterado.',
                   )

    return False


@app.route('/descargarPO/<id>',methods=['GET'])
def descargarPO(id):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'Traducido',
        'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    #----------------------------------------------------------------
    cursor = connection.cursor()
    cursor.execute('SELECT Complemento, Localizacion, Cadena FROM ArchivoCadena WHERE idDetalleArchivo='+ id)
    results = [{"Complemento":Complemento, "Localizacion": Localizacion,"Cadena": Cadena} for (Complemento, Localizacion, Cadena) in cursor]
    cursor.close()
    connection.close()
    #----------------------------------------------------------------
    localpath = "pfiles/"
    complete = localpath + "ERR.po"
    semicomplete = "ERR.po"
    tipo = ".po"
    #----------------------------------------------------------------
    j = json.dumps({'result':results})
    try:
        decoded = json.loads(j)
        for x in decoded['result']:
            name = x['Complemento'].replace(" ", "_")
            localizacion = x['Localizacion']
            nameFile = name + "-" + localizacion
            complete = localpath + nameFile + tipo
            semicomplete = nameFile + tipo
            po = polib.POFile()
            po.metadata = {
                'Project-Id-Version': '1.0',
                'Report-Msgid-Bugs-To': 'you@example.com',
                'POT-Creation-Date':  time.strftime("%c"),
                'PO-Revision-Date':  time.strftime("%c"),
                'Last-Translator': '<you@example.com>',
                'Language-Team': '<yourteam@example.com>',
                'MIME-Version': '1.0',
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Transfer-Encoding': '8bit',
                }
            decodedextra = json.loads(x['Cadena'])
            for y in decodedextra:
                entry = polib.POEntry(
                    msgid= y['msgid'],
                    msgstr=y['msgstr'],
                    occurrences=[('welcome.py', '12'), ('anotherfile.py', '34')]
                    )
                po.append(entry)
            po.save(complete)
    except (ValueError, KeyError, TypeError):
        print("JSON format error", file=sys.stderr)
        return redirect('/listarComplementos')
    #----------------------------------------------------------------
    return redirect(url_for('get_file', path=semicomplete))

@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@app.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


@app.route('/descargarMO/<id>',methods=['GET'])
def descargarMO(id):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'Traducido',
        'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    #----------------------------------------------------------------
    cursor = connection.cursor()
    cursor.execute('SELECT Complemento, Localizacion FROM ArchivoCadena WHERE idDetalleArchivo='+ id)
    results = [{"Complemento":Complemento, "Localizacion": Localizacion} for (Complemento, Localizacion) in cursor]
    cursor.close()
    connection.close()
    #----------------------------------------------------------------
    localpath = "pfiles/"
    complete = localpath + "ERR.mo"
    nameFile = "ERR"
    semicomplete = "ERR.mo"
    tipoMO = ".mo"
    tipoPO = ".po"
    #----------------------------------------------------------------
    j = json.dumps({'result':results})
    try:
        decoded = json.loads(j)
        for x in decoded['result']:
            name = x['Complemento'].replace(" ", "_")
            localizacion = x['Localizacion']
            nameFile = name + "-" + localizacion
            complete = localpath + nameFile + tipoMO
            semicomplete = nameFile + tipoMO
    except (ValueError, KeyError, TypeError):
        print("JSON format error", file=sys.stderr)
        return redirect('/listarComplementos')
    #----------------------------------------------------------------
    completePO = localpath + nameFile + tipoPO
    po = polib.pofile(completePO)
    po.save_as_mofile(complete)
    return redirect(url_for('get_file', path=semicomplete))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
