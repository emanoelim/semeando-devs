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
        """
        Recupera todos os livros
        ---
        tags:
          - livros
        responses:
          200:
            description: lista de livros
        """
        livros = Livro.list()
        resposta = {
            'dados': [livro.serialize() for livro in livros]
        }
        return resposta, 200
    
    def post(self):
        """
        Adicionar livro
        ---
        tags:
          - livros
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                titulo:
                  type: string
                ano:
                  type: integer
                autor_id:
                  type: integer
        responses:
          201:
            description: livro criado
          400:
            description: dados inválidos
        """
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
        """
        Recuperar livro
        ---
        tags:
          - livros
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: livro
          404:
            description: livro não encontrado
        """
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
        """
        Atualizar livro
        ---
        tags:
          - livros
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
                titulo:
                  type: string
                ano:
                  type: integer
                autor_id:
                  type: integer
        responses:
          200:
            description: livro atualizado
          400:
            description: dados inválidos
          404: 
            description: livro não encontrado
        """
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
        """
        Deletar livro
        ---
        tags:
          - livros
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          204:
            description: livro deletado
          404:
            description: livro não encontrado
        """
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
