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
        """
        Recupera todos os autores
        ---
        tags:
          - autores
        responses:
          200:
            description: lista de autores
        """
        autores = Autor.list()
        resposta = {
            'dados': [autor.serialize() for autor in autores]
        }
        return resposta, 200
    
    def post(self):
        """
        Adicionar autor
        ---
        tags:
          - autores
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                data_nascimento:
                  type: string
        responses:
          201:
            description: autor criado
          400:
            description: dados inválidos
        """
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
        """
        Recuperar autor
        ---
        tags:
          - autores
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: autor
          404:
            description: autor não encontrado
        """
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
        """
        Atualizar autor
        ---
        tags:
          - autores
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                data_nascimento:
                  type: string
        responses:
          200:
            description: autor atualizado
          400:
            description: dados inválidos
          404: 
            description: autor não encontrado
        """
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
        """
        Deletar autor
        ---
        tags:
          - autores
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          204:
            description: autor deletado
          404:
            description: autor não encontrado
        """
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
