from flask import Flask, request
from db import db
from livros import Livro


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livro.db'


# /livros - POST, GET
@app.route("/livros", methods=['GET', 'POST'])
def livros(): 
    if request.method == 'GET':
        livros = Livro.list()
        resposta = {
            'dados': [livro.serialize() for livro in livros]
        }
        return resposta, 200
    
    else:
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        ano = request_data.get('ano')
        livro = Livro(titulo, ano)
        livro.save()
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 201


# /livros/id - GET, PUT, DELETE
@app.route("/livros/<id>", methods=['GET', 'PUT', 'DELETE'])
def livros_id(id):
    livro = Livro.retrieve(int(id))
    if not livro:
        resposta = {
            'dados': []
        }
        return resposta,  404

    if request.method == 'GET':
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 200
    
    elif request.method == 'PUT':
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        ano = request_data.get('ano')
        livro.titulo = titulo
        livro.ano = ano
        livro.save()
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 200

    else:
        livro.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204


if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()