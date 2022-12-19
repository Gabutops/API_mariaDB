import json
from flask import Flask, make_response,request,jsonify, render_template, jsonify, abort
from markupsafe import escape
from controller.search import Search
import mysql.connector
from flask_cors import CORS

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '',
    database = 'banco de dados'
)

app = Flask(__name__)
CORS(app)
from flask import send_from_directory

@app.route('/reports/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)

@app.route('/')
def get_infos():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM bd') 
    meus_dados = my_cursor.fetchall()
    dados = list()
    for dado in meus_dados:
        dados.append(
            {
                'id':dado[0],
                'RNA_Seq':dado[1],
                'Laudo':dado[2],
                'Lamina':dado[3]
            }
        )
    return make_response(
        jsonify(
            mensagem = 'Consulta realizada com sucesso!',
            dados = meus_dados
        )
    )



@app.route('/', methods = ['POST'])
def create_data():
    data = request.json
    my_cursor = mydb.cursor()
    
    sql = f"INSERT INTO bd (RNA_Seq, Laudo, Lamina) VALUES ('{data['RNA_Seq']}','{data['Laudo']}','{data['Lamina']}')"
    
    my_cursor.execute(sql) 
    mydb.commit()
    return make_response(
        jsonify(
            mensagem = 'Dados cadastrados com sucesso',
            dados = data
        )
    )

@app.route("/id/<id>", methods = ['GET'])
def get_id(id):
    my_cursor = mydb.cursor()
    my_cursor.execute(f'SELECT * FROM bd WHERE ID = {id}')
    meus_dados = my_cursor.fetchall()
    dados = list()
    for dado in meus_dados:
        dados.append(
            {
                'id':dado[0],
                'RNA_Seq':dado[1],
                'Laudo':dado[2],
                'Lamina':dado[3]
            }
        )
    return make_response(
        jsonify(
            mensagem = 'Consulta realizada com sucesso!',
            dados = meus_dados
        )
    )

if __name__ == '__main__':  # pragma: no cover
    app.run(port=5000)