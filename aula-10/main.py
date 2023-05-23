from flask import Flask, request
from db import db
from livros import Livro
from autores import Autor


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/postgres'

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
        autor_id = request_data.get('autor_id')
        livro = Livro(titulo, ano, autor_id)
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
        autor_id = request_data.get('autor_id')
        livro.titulo = titulo
        livro.ano = ano
        livro.autor_id = autor_id
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
    
# /autores - POST, GET
@app.route("/autores", methods=['GET', 'POST'])
def autores(): 
    if request.method == 'GET':
        autores = Autor.list()
        resposta = {
            'dados': [autor.serialize() for autor in autores]
        }
        return resposta, 200
    
    else:
        request_data = request.get_json()
        nome = request_data.get('nome')
        data_nascimento = request_data.get('data_nascimento')
        autor = Autor(nome, data_nascimento)
        autor.save()
        resposta = {
            'dados': [autor.serialize()]
        }
        return resposta, 201


# /autores/id - GET, PUT, DELETE
@app.route("/autores/<id>", methods=['GET', 'PUT', 'DELETE'])
def autores_id(id):
    autor = Autor.retrieve(int(id))
    if not autor:
        resposta = {
            'dados': []
        }
        return resposta,  404

    if request.method == 'GET':
        resposta = {
            'dados': [autor.serialize()]
        }
        return resposta, 200
    
    elif request.method == 'PUT':
        request_data = request.get_json()
        nome = request_data.get('nome')
        data_nascimento = request_data.get('data_nascimento')
        autor.nome = nome
        autor.data_nascimento = data_nascimento
        autor.save()
        resposta = {
            'dados': [autor.serialize()]
        }
        return resposta, 200

    else:
        autor.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204


if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()