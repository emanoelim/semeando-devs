from flask_restful import Resource, reqparse

from livro.livros import Livro


parser = reqparse.RequestParser()
parser.add_argument(
    'livro_id',
    type=int,
    required=False
)
parser.add_argument(
    'titulo',
    type=str,
    required=True,
    help='Título inválido.'
)
parser.add_argument(
    'ano',
    type=int,
    required=True,
    help='Ano inválido.'
)
parser.add_argument(
    'autor_id',
    type=int,
    required=True,
    help='Autor id inválido.'
)


class LivroListResource(Resource):
    def get(self):
        livros = Livro.list()
        resposta = {
            'dados': [livro.serialize() for livro in livros]
        }
        return resposta, 200
    
    def post(self):
        request_data = parser.parse_args()
        titulo = request_data.get('titulo')
        ano = request_data.get('ano')
        autor_id = request_data.get('autor_id')
        livro = Livro(titulo, ano, autor_id)
        livro.save()
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 201
    

class LivroResource(Resource):
    def get(self, id):
        livro = Livro.retrieve(int(id))
        if not livro:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 200
        
    def put(self, id):
        livro = Livro.retrieve(int(id))
        if not livro:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        request_data = parser.parse_args()
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
    
    def delete(self, id):
        livro = Livro.retrieve(int(id))
        if not livro:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        livro.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204
