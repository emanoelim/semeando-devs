from flask_restful import Resource, reqparse

from autor.autores import Autor


parser = reqparse.RequestParser()
parser.add_argument(
    'autor_id',
    type=int,
    required=False
)
parser.add_argument(
    'nome',
    type=str,
    required=True,
    help='Nome inválido.'
)
parser.add_argument(
    'data_nascimento',
    type=str,
    required=True,
    help='Data de nascimento inválido.'
)


class AutorListResource(Resource):
    def get(self):
        autores = Autor.list()
        resposta = {
            'dados': [autor.serialize() for autor in autores]
        }
        return resposta, 200
    
    def post(self):
        request_data = parser.parse_args()
        nome = request_data.get('nome')
        data_nascimento = request_data.get('data_nascimento')
        autor = Autor(nome, data_nascimento)
        autor.save()
        resposta = {
            'dados': [autor.serialize()]
        }
        return resposta, 201
    

class AutorResource(Resource):
    def get(self, id):
        autor = Autor.retrieve(int(id))
        if not autor:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        resposta = {
            'dados': [autor.serialize()]
        }
        return resposta, 200
    
    def put(self, id):
        autor = Autor.retrieve(int(id))
        if not autor:
            resposta = {
                'dados': []
            }
            return resposta,  404

        request_data = parser.parse_args()
        nome = request_data.get('nome')
        data_nascimento = request_data.get('data_nascimento')
        autor.nome = nome
        autor.data_nascimento = data_nascimento
        autor.save()
        resposta = {
            'dados': [autor.serialize()]
        }
        return resposta, 200

    def delete(self, id):
        autor = Autor.retrieve(int(id))
        if not autor:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        autor.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204
