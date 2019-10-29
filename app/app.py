from typing import List, Dict
from flask import Flask
import mysql.connector
import json

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
