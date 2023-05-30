# Aula 11

## Reorganizando o projeto

Na próxima aula vamos adicionar mais duas classes: Cliente e Pedido. O arquivo main.py já está ficando grande e difícil de dar manutenção. Desta forma, vamor quebrar o projeto em alguns arquivos antes de criar as novas classes.

Incialmente, vamos criar a pasta "livro" e "autor" e mover as respectivas classes para dentro delas.

Vamos fazer a instalação de uma nova biblioteca, a https://pypi.org/project/Flask-RESTful/, que vai facilitar ainda mais a criação dos endpoints.

- `pip install Flask-RESTful`

Dentro da pasta livro, vamos criar o arquivo resources.py. Vamos criar a classe LivroListResource (para o post e o get todos) e a classe LivroResource (para o get, put e delete). Ambas herdam da classe Resource. 

A classe Resource permite criar métodos com os nomes http, como get(), post(), put() e delete(), em vez de termos uma única função que trata cada um desses métodos por meio de uma estrutura de decisão. 

Desta forma, todas as lógicas referentes ao livro no main.py podem ser extraídas para métodos nessas classes:

```python
from flask_restful import Resource, reqparse

from livro.livros import Livro

"""
Não vamos mais conseguir pegar os parâmetros da chamada através de: request_data = request.get_json(). Vamos precisar de um parser.
Este parser ficará disponível para todas as classes do arquivo.
Nele adicionamos os parâmetros que o usuário poderá enviar na chamada.
"""
parser = reqparse.RequestParser()
parser.add_argument('livro_id')
parser.add_argument('titulo')
parser.add_argument('ano')
parser.add_argument('autor_id')


class LivroListResource(Resource):
    def get(self):
        livros = Livro.list()
        resposta = {
            'dados': [livro.serialize() for livro in livros]
        }
        return resposta, 200
    
    def post(self):
        request_data = parser.parse_args()  # ANTES: request_data = request.get_json()
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
```

No main.py, podemos remover os métodos livros() e livros_id(). Vamos fazer o mapeamento com as classes LivroListResource e LivroResource:

```python
from flask import Flask, request
from flask_restful import Api

from db import db
from livro.resources import LivroListResource, LivroResource
from autor.autores import Autor


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/postgres'

# Mapeamento com as classes LivroResource e LivroListResource
api = Api(app)
api.add_resource(LivroResource, '/livros/<id>')  # o /id primeiro!
api.add_resource(LivroListResource, '/livros/')

    
# /autores - POST, GET
@app.route("/autores", methods=['GET', 'POST'])
def autores(): 
    ...
```

Fazendo o mesmo com os autores, teremos o resources.py do autor:

```python
from flask_restful import Resource, reqparse

from autor.autores import Autor


parser = reqparse.RequestParser()
parser.add_argument('autor_id')
parser.add_argument('nome')
parser.add_argument('data_nascimento')


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

```

Obs.: na classe Autor, foi necessário ajustar o serialize, para não ter problema com o tipo data:

```python
    def serialize(self):
        return {
            'autor_id': self.autor_id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.isoformat()  # AQUI
        }
```

E o arquivo main.py, ficará:

```python
from flask import Flask, request
from flask_restful import Api

from db import db
from livro.resources import LivroListResource, LivroResource
from autor.resources import AutorListResource, AutorResource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/postgres'

api = Api(app)
api.add_resource(LivroResource, '/livros/<id>')
api.add_resource(LivroListResource, '/livros/')
api.add_resource(AutorResource, '/autores/<id>')
api.add_resource(AutorListResource, '/autores/')


if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()
```

### Adicionando validações

O parser pode ser utilizado para validar os dados no post / put. 

Vamos atualizar o parser do autor para:

```python
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
```

Caso você tente adicionar um autor sem data de nascimento, por exemplo, deve receber um erro 400 com a seguinte mensagem:

```json
{
	"message": {
		"data_nascimento": "Data de nascimento inválido."
	}
}
```

O mesmo pode ser feito com o parser do livro:

```python
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
```

Caso você tente adicionar um livro com um autor_id que seja do tipo string, por exemplo, deve ter um erro:

```json
{
	"message": {
		"autor_id": "Autor id inválido."
	}
}
```

### Retornando os dados do autor no livro

O ajuste abaixo na classe Livro retornará as informações do autor juntamente com o livro, em vez de retornar apenas o autor_id:

```python
    def serialize(self):
        autor = Autor.retrieve(self.autor_id)
        dados_autor = autor.serialize() if autor else None  # if ternário
        return {
            'livro_id': self.livro_id,
            'titulo': self.titulo,
            'ano': self.ano,
            'autor': dados_autor
        }
```

O if ternário é equivalente a:

```python
if autor:
    dados_autor = autor.serialize()
else:
    dados_autor = None
```