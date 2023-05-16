
# Aula 9

## Banco de dados 

Um banco de dados é uma coleção organizada de informações - ou dados - estruturadas, normalmente armazenadas eletronicamente em um sistema de computador. Um banco de dados é geralmente controlado por um sistema de gerenciamento de banco de dados (DBMS) (https://www.oracle.com/br/database/what-is-database/).

Estes dados podem ser organizados no formato de tabelas, semelhante a um csv. Este é o caso dos bancos de dados **relacionais**:

| livro_id | titulo              | ano_lancamento  | paginas | autor            |
|----------|---------------------|------|---------|------------------|
| 1        | A Sociedade do Anel | 2022 | 200     | J. R. R. Tolkien |
| 2        | As Duas Torres      | 2022 | 250     | J. R. R. Tolkien |
| 3        | O Retorno do Rei    | 2022 | 300     | J. R. R. Tolkien |


Este formato é fácil de ser representado como uma classe Python:

```python
class Livro:
    def __init__(self, livro_id, titulo, ano_lancamento, paginas, autor):
        self.livro_id = livro_id
        self.titulo = titulo
        self.ano_lancamento = ano_lancamento
        self.paginas = paginas
        self.autor = autor
```

Para realizar operações de criar / atualizar / recuperar / excluir dados das tabelas, precisamos executar alguns comandos, através da linguagem **SQL** (Structured Query Language - Linguagem de consulta estruturada).

O SQL é uma linguagem de programação usada por quase todos os bancos relacionais para consultar / manipular os dados.

A depender do SGDB utilizado, podem existir algumas diferenças no SQL, mas em geral será bem parecido.

### Exemplo de criação de uma tabela

```sql
CREATE TABLE livro (
   livro_id INTEGER PRIMARY KEY,
   titulo VARCHAR(255),
   ano INTEGER
);
```

Cada linha dentro do bloco acima será uma coluna da tabela. Ao lado do nome da coluna é necessário informar seu tipo. A primeira coluna é ainda identificada como PRIMARY KEY e será um identificador único para cada livro.

### Exemplo de inserção de dados

```sql
INSERT INTO livro(titulo, ano) VALUES ('A Sociedade do Anel', '2022')
INSERT INTO livro(titulo, ano) VALUES ('As Duas Torres', '2022')
INSERT INTO livro(titulo, ano) VALUES ('O Retorno do Rei', '2022')
```

É necessário informar em qual tabela os dados serão adicionados, bem como as colunas que receberão as informações e os valores que vão em cada coluna.

### Exemplo de recuperação de dados

```sql
select * from livro
select * from livro where livro_id = 2
select * from livro where titulo = 'As Duas Torres'
select * from livro where titulo like '%Duas Torres%'
```

Onde:
1. Seleciona todos os livros;
2. Seleciona um livro com id específico;
3. Seleciona um livro com nome específico;
4. Seleciona um livro cujo nome contém uma certa string.

### Exemplo de exclusão de dados

```sql
DELETE FROM livro WHERE livro_id = 3
```

**IMPORTANTE**: nunca esquecer o WHERE ao fazer o DELETE, caso contrário serão excluídos todos os dados da tabela!


## API Flask com persistência de dados

Neste app, os dados ficarão salvos no banco, então não serão perdidos cada vez que ele for executado novamente.

Ainda não utilizaremos um SGDB. Vamos utilizar o módulo **sqlite3**, do python, para executar os comandos para manipular o banco.

### Configurando o projeto
- Criar uma pasta chamada flask.
- Abrir um terminal na pasta criada.
- Criar uma virtualenv: python -m venv .venv.
- Ativar a venv: .venv/bin/activate
- Instalar a lib flask: pip intall flask.
- Isntalar a lib SQLAlchemy: pip install flask_sqlalchemy, que vai facilitar as operações no banco de dados.
- Instalar a lib requests, para testar as  chamadas: pip install requests.


### Definindo o banco de dados

O python já possui um módulo chamado sqlite3. Ele implementa um banco de dados leve, embutido na aplicação, sem a necessidade de instalar separada um servidor de banco de dados. É muito usado aplicativos mobile e também durante testes.

```different
import sqlite3
conn = sqlite3.connect("livro.db")
```

Criando a tabela **Livro**:
```different
create_table_cmd = """
CREATE TABLE livro (
   livro_id INTEGER PRIMARY KEY,
   titulo VARCHAR(255),
   ano INTEGER
);
"""
conn.execute(create_table_cmd)
```

Adicionando alguns livros:

```different
add_l1_cmd = "INSERT INTO livro(titulo, ano) VALUES ('A Sociedade do Anel', 2022)"
add_l2_cmd = "INSERT INTO livro(titulo, ano) VALUES ('As Duas Torres', 2022)"
add_l3_cmd = "INSERT INTO livro(titulo, ano) VALUES ('O Retorno do Rei', 2022)"
conn.execute(add_l1_cmd)
conn.execute(add_l2_cmd)
conn.execute(add_l3_cmd)
```

Selecionando todos os livros:

```different
select_cmd = 'select * from livro'
cur = conn.cursor()
cur.execute(select_cmd)
livros = cur.fetchall()
livros[0], livros[1], livros[2]
```

Selecionando um  livro de acordo com uma coluna:

```different
select_cmd = 'select * from livro where livro_id = 1'
cur.execute(select_cmd)
livro = cur.fetchall()
livro[0]
```

Atualizando um livro:

```different
update_cmd = 'UPDATE livro SET ano = 2020 WHERE livro_id = 1'
conn.execute(update_cmd)
select_cmd = 'select * from livro where livro_id = 1'
cur.execute(select_cmd)
livro = cur.fetchall()
livro[0]
```

### Definindo a classe Livro

Em um arquivo livros.py criar a classe **Livro** que será um espelho da tabela:

```python
class Livro:
    def __init__(self, livro_id, titulo, ano):
        self.livro_id = livro_id
        self.titulo = titulo
        self.ano = ano

    def serialize(self):
        return {
            'livro_id': self.livro_id,
            'titulo': self.titulo,
            'ano': self.ano
        }
    
    # Método para o GET (todos)
    def list(self):
        pass

    # Método para o GET
    def retrieve(self):
        pass

    # Método para o POST
    def create(self):
        pass

    # Método para o PUT
    def update(self):
        pass

    # Método para o DELETE
    def delete(self):
        pass
``` 

Também vamos criar o "esqueleto" do main.py:

```python
from flask import Flask, request
from livros import Livro


app = Flask(__name__)


# /livros - POST, GET
@app.route("/livros", methods=['GET', 'POST'])
def livros(): 
    if request.method == 'GET':
        pass
    
    else:
        pass


# /livros/id - GET, PUT, DELETE
@app.route("/livros/<id>", methods=['GET', 'PUT', 'DELETE'])
def livros_id(id):
    if request.method == 'GET':
        pass
    
    elif request.method == 'PUT':
        pass

    else:
        pass


if __name__ == '__main__':
    app.run()
```

### Preparando a aplicação para conectar no banco

Criar um arquivo db.py:

```python
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
```

Atualizar o arquivo main.py:

```python
from flask import Flask, request
from db import db  # NOVA LINHA
from livros import Livro


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livro.db'  # NOVA LINHA


# /livros - POST, GET
@app.route("/musicas", methods=['GET', 'POST'])
def livros(): 
    if request.method == 'GET':
        pass
    
    else:
        pass


# /livros/id - GET, PUT, DELETE
@app.route("/livros/<id>", methods=['GET', 'PUT', 'DELETE'])
def livros_id(id):
    if request.method == 'GET':
        pass
    
    elif request.method == 'PUT':
        pass

    else:
        pass


if __name__ == '__main__':
    db.init_app(app)  # NOVA LINHA

    # NOVO BLOCO
    with app.app_context():
        db.create_all()
    # FIM NOVO BLOCO

    app.run()
```

A classe Livro também precisará ser alterada:

```python
class Livro(db.Model):
    # NOVO BLOCO
    __tablename__ = 'livro'

    livro_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    ano = db.Column(db.Integer)
    # FIM NOVO BLOCO

    def __init__(self, titulo, ano):
        self.titulo = titulo
        self.ano = ano
```

### Salvando um livro

Vamos adicionar o import abaixo no arquivo da classe Livro:

```python
from db import db
```

Na classe Livro, implementar o método create:

```python
    # Método para o POST
    def create(self):
        db.session.add(self)
        db.session.commit()
```

No main.py, adicionar a lógica do POST:

```python
# /livros - POST, GET
@app.route("/livros", methods=['GET', 'POST'])
def livros(): 
    if request.method == 'GET':
        pass
    
    else:
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        ano = request_data.get('ano')
        livro = Livro(titulo, ano)
        livro.create()
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 201
```

Utilizando a lib requests para testar:

```different
requests.post(url='http://127.0.0.1:5000/livros', json={'titulo': 'Lugar Nenhum', 'ano': 2020}, headers={'Content-type': 'application/json'})
```

### Recuperando todos os livros

Neste caso, o método foi alterado para ser um **classmethod**, assim não precisamos ter um objeto instanciado para poder chama-lo:

```python
    # Método para o GET (todos)
    @classmethod
    def list(cls):
        return cls.query.all()
```

E no main.py:

```python
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
        livro.create()
        resposta = {
            'dados': [livro.serialize()]
        }
        return resposta, 201
```

Para testar, basta acessar http://127.0.0.1:5000/livros.

### Recuperando um livro

Na classe Livro:

```python
    # Método para o GET
    @classmethod
    def retrieve(cls, id):
        return cls.query.filter_by(livro_id=id).first()
```

No main.py, adicionar a lógica do GET e também o tratamento para caso não encontre nada:

```python
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
        pass

    else:
        pass
```

### Excluindo um livro

Na classe Livro:

```python
    # Método para o DELETE
    def delete(self):
        db.session.delete(self)
        db.session.commit()
```

No main.py, implementar a lógica do DELETE:

```python
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
        pass

    else:
        livro.delete()
        resposta = {
            'dados': []
        }
        return resposta, 204
```

Para testar:

```different
requests.delete(url='http://127.0.0.1:5000/livros/2')
```

### Atualizando um livro

A lógica será a mesma do create:

```python
    # Método para o PUT
    def update(self):
        db.session.add(self)
        db.session.commit()
```

E no main.py:

```python
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
        livro.update()
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
```

Para testar:

```different
requests.put(url='http://127.0.0.1:5000/livros/1', json={'titulo': 'Lugar nenhum', 'ano': 2020}, headers={'Content-type': 'applicat
ion/json'})
```

(Foi alterado de "Lugar Nenhum" para "Lugar nenhum").

Como o create() e o update() ficaram iguais, podemos juntar em só método chamado save():

```python
    # Método para o POST / UPDATE
    def save(self):
        db.session.add(self)
        db.session.commit()
```

Atualizar também no main.py:

```python
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
        livro.save()  # Atualizado de create para save
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
        livro.save()  # Atualizado de update para save
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
```