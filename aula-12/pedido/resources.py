from flask_restful import Resource, reqparse

from pedido.pedidos import Pedido
from pedido.validators import livro_valido
from livro.livros import Livro


parser = reqparse.RequestParser()
parser.add_argument(
    'pedido_id',
    type=int,
    required=False
)
parser.add_argument(
    'cliente_id',
    type=int,
    required=True,
    help='Cliente id inválido.'
)
parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Data inválido.'
)


parser_livro_pedido = reqparse.RequestParser()
parser_livro_pedido.add_argument(
    'livro_id',
    type=livro_valido,
    required=True,
    help='Livro id inválido.'
)


class PedidoListResource(Resource):
    def get(self):
        """
        Recupera todos os pedidos
        ---
        tags:
          - pedidos
        responses:
          200:
            description: lista de pedidos
        """
        pedidos = Pedido.list()
        resposta = {
            'dados': [pedido.serialize() for pedido in pedidos]
        }
        return resposta, 200
    
    def post(self):
        """
        Adicionar pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                cliente_id:
                  type: integer
                data:
                  type: string
        responses:
          201:
            description: pedido criado
          400:
            description: dados inválidos
        """
        request_data = parser.parse_args()
        cliente_id = request_data.get('cliente_id')
        data = request_data.get('data')
        pedido = Pedido(cliente_id, data)
        pedido.save()
        resposta = {
            'dados': [pedido.serialize()]
        }
        return resposta, 201
    

class PedidoResource(Resource):
    def get(self, id):
        """
        Recuperar pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: pedido
          404:
            description: pedido não encontrado
        """
        pedido = Pedido.retrieve(int(id))
        if not pedido:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        resposta = {
            'dados': [pedido.serialize()]
        }
        return resposta, 200
    
    def put(self, id):
        """
        Atualizar pedido
        ---
        tags:
          - pedidos
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
                cliente_id:
                  type: integer
                data:
                  type: string
        responses:
          200:
            description: pedido atualizado
          400:
            description: dados inválidos
          404: 
            description: pedido não encontrado
        """
        pedido = Pedido.retrieve(int(id))
        if not pedido:
            resposta = {
                'dados': []
            }
            return resposta,  404

        request_data = parser.parse_args()
        cliente_id = request_data.get('cliente_id')
        data = request_data.get('data')
        pedido.cliente_id = cliente_id
        pedido.data = data
        pedido.save()
        resposta = {
            'dados': [pedido.serialize()]
        }
        return resposta, 200

    def delete(self, id):
        """
        Deletar pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          204:
            description: pedido deletado
          404:
            description: pedido não encontrado
        """
        pedido = Pedido.retrieve(int(id))
        if not pedido:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        pedido.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204


class LivroPedidoListResource(Resource):
    def get(self, id):
        """
        Recupera todos os livros do pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: lista de livros do pedido
        """
        pedido = Pedido.retrieve(id)
        if not pedido:
            resposta = {
                'dados': []
            }
            return resposta,  404


        livros = pedido.livros
        dados_livros = [livro.serialize() for livro in livros] 
        resposta = {
            'dados': dados_livros
        }
        return resposta, 200
    
    def post(self, id):
        """
        Adicionar livro ao pedido
        ---
        tags:
          - pedidos
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
                livro_id:
                  type: integer
        responses:
          201:
            description: livro adicionado ao pedido
          400:
            description: dados inválidos
        """
        pedido = Pedido.retrieve(id)
        if not pedido:
            resposta = {
                'dados': []
            }
            return resposta,  404
        
        request_data = parser_livro_pedido.parse_args()
        livro = request_data.get('livro_id')
        pedido.livros.append(livro)
        pedido.save()
        resposta = {
            'dados': [pedido.serialize()]
        }
        return resposta, 201
    

class LivroPedidoResource(Resource):
    def get(self, id, livro_id):
        """
        Recupera um livro do pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - name: livro_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: livro do pedido
        """
        pass
    
    def put(self, id, livro_id):
        """
        Atualiza um livro do pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - name: livro_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: livro atualizado
          400:
            description: dados inválidos
        """
        pass
    
    def delete(self, id, livro_id):
        """
        Deleta um livro do pedido
        ---
        tags:
          - pedidos
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - name: livro_id
            in: path
            type: integer
            required: true
        responses:
          204:
            description: livro deletado
          404:
            description: livro não encontrado
        """
        pass