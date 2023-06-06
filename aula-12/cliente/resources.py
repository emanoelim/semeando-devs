from flask_restful import Resource, reqparse

from cliente.clientes import Cliente
from cliente.validators import cpf_valido


parser = reqparse.RequestParser()
parser.add_argument(
    'cliente_id',
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
    'cpf',
    type=cpf_valido,
    required=True,
    help='CPF inválido.'
)
parser.add_argument(
    'data_nascimento',
    type=str,
    required=True,
    help='Data de nascimento inválido.'
)


class ClienteListResource(Resource):
    def get(self):
        """
        Recupera todos os clientes
        ---
        tags:
          - clientes
        responses:
          200:
            description: lista de clientes
        """
        clientes = Cliente.list()
        resposta = {
            'dados': [cliente.serialize() for cliente in clientes]
        }
        return resposta, 200
    
    def post(self):
        """
        Adicionar cliente
        ---
        tags:
          - clientes
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                cpf:
                  type: string
                data_nascimento:
                  type: string
        responses:
          201:
            description: cliente criado
          400:
            description: dados inválidos
        """
        request_data = parser.parse_args()
        nome = request_data.get('nome')
        cpf = request_data.get('cpf')
        data_nascimento = request_data.get('data_nascimento')
        cliente = Cliente(nome, cpf, data_nascimento)
        cliente.save()
        resposta = {
            'dados': [cliente.serialize()]
        }
        return resposta, 201
    

class ClienteResource(Resource):
    def get(self, id):
        """
        Recuperar cliente
        ---
        tags:
          - clientes
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: cliente
          404:
            description: cliente não encontrado
        """
        cliente = Cliente.retrieve(int(id))
        if not cliente:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        resposta = {
            'dados': [cliente.serialize()]
        }
        return resposta, 200
    
    def put(self, id):
        """
        Atualizar cliente
        ---
        tags:
          - clientes
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
                cpf:
                  type: string
                data_nascimento:
                  type: string
        responses:
          200:
            description: cliente atualizado
          400:
            description: dados inválidos
          404: 
            description: cliente não encontrado
        """
        cliente = Cliente.retrieve(int(id))
        if not cliente:
            resposta = {
                'dados': []
            }
            return resposta,  404

        request_data = parser.parse_args()
        nome = request_data.get('nome')
        cpf = request_data.get('cpf')
        data_nascimento = request_data.get('data_nascimento')
        cliente.nome = nome
        cliente.data_nascimento = data_nascimento
        cliente.save()
        resposta = {
            'dados': [cliente.serialize()]
        }
        return resposta, 200

    def delete(self, id):
        """
        Deletar cliente
        ---
        tags:
          - clientes
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          204:
            description: cliente deletado
          404:
            description: cliente não encontrado
        """
        cliente = Cliente.retrieve(int(id))
        if not cliente:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        cliente.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204
