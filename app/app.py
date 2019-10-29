from typing import List, Dict
from flask import Flask,render_template,request,jsonify
import mysql.connector
import json
import jwt

app = Flask(__name__)


def usuarios() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tareaSA',
        'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM usuarios')
    results = [{nombre: apellido} for (nombre, apellido) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    return json.dumps({'usuarios': usuarios()})


@app.route('/prueba')
def prueba() -> str:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tareaSA',
        'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM usuarios')
    results = [{"nombre": nombre, "apellido" : apellido} for (nombre, apellido) in cursor]
    cursor.close()
    connection.close()

    #return results
    #return json.dumps({'usuarios': usuarios()})

    return render_template('index.html', data=results)



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


    print(nombre_usuario)
    print(correo_usuario)
    print(complemento)









    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tareaSA',
        'auth_plugin':'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM usuarios')
    results = [{"nombre": nombre, "apellido" : apellido} for (nombre, apellido) in cursor]
    cursor.close()
    connection.close()

    #return results
    #return json.dumps({'usuarios': usuarios()})

    return render_template('index.html', data=results)




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



if __name__ == '__main__':
    app.run(host='0.0.0.0')
