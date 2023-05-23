
# Aula 10

## Postgres e relacionamento entre tabelas 

Ferramentas utilizadas:
- Postgres: https://www.postgresql.org/;
- DBeaver: https://dbeaver.io/download/.
- Docker: https://www.docker.com/products/docker-desktop/;

### Postgres
É um sistema de banco de dados relacional open source. Já conta com mais de 35 anos, sendo um dos sistemas mais utilizados.

### DBeaver
É um aplicativo para administração de banco de dados universal, suportando vários tipos de banco de dados, como Postgres, MySQL, SQLite, Redis, etc.

Como ele conseguimos executar comandos SQL, visualizar os dados e até mesmo ver um diagrama do banco, entre outros.

### Docker
É uma ferramenta open source para containerização. 

Um conteiner é um ambiente isolado. Ele contém um conjunto de processos que são executados a partir de uma imagem. Essas imagens podem ser encontradas aqui: https://hub.docker.com/search?q=postgres.

Os containeres utilizam o mesmo kernel do sistema operacional, mas ficam isolados uns dos outros e também do restante do sistema. Por exemplo: em vez de você instalar o Postgres diretamente no sistema operacional, você pode rodar ele a partir de um conteiner. Você pode até ter vários containeres do Postgres, cada um baseado em uma imagem diferente.

Com o auxílio do docker também é possível criar suas próprias imagens. Exemplo: uma imagem que contenha todas as dependências deste projeto, incluindo o banco de dados, as bibliotecas Python, como o Flask e etc. Qualquer pessoa com esta imagem deve conseguir rodar o projeto dentro de containeres, da mesma maneira que você, independente do seu sistema operacional.

### Atualizando o projeto para utilizar o Postgres

Iniciar um conteiner com o Postgres: `docker run --name pg-flask -p 5433:5432 -e POSTGRES_PASSWORD=postgres postgres`.

Onde:
- --name define o nome do conteiner.
- -p 5433:5432 faz o mapeamento da porta 5432 do conteiner para a porta 5433 do localhost. Isto foi feito para evitar conflitos, visto que muitas vezes o Postgres já está instalado diretamente no localhost e rodando na porta 5432.

- -e permite definir variáveis como username e senha para o banco.

- O último parâmetro é nome da imagem que será baixado do docker hub para ser utilizada como base do conteiner.

Será apresentado um logo semelhante a este:
```different
2023-05-21 13:28:51.897 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
```

Com a venv ativada, instalar a dependência: `pip install psycopg2-binary`.

Alterar a config do banco no projeto para:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/postgres'
```

Onde postgres:postgres indica banco:senha.

Ao salvar e rodar a aplicação novamente, deve rodar sem erros.

Em um terminal Python, deve ser possível registrar um novo livro:
```python
requests.post(url='http://127.0.0.1:5000/livros', json={'titulo': 'Lugar Nenhum', 'ano': 2020}, headers={'Content-type': 'applicati
on/json'})
```

### Conectando no banco com DBeaver

1. Clicar no ícone de nova conexão:

![1](figuras/1.png)

2. Selecionar o banco:

![2](figuras/2.png)

3. Caso solicite, fazer o download das dependências:

![3](figuras/3.png)

4. Preencher com os dados do conteiner do Postgres e depois clicar em "Testar conexão". Caso dê sucesso, concluir.

![4](figuras/4.png)

5. Verificar que a tabela foi criada e que foi adicionado o livro:

![5](figuras/5.png)


### Adicionando autores

Criar a classe **Autor** em um novo arquivo **autores.py**:

```python
from db import db


class Autor(db.Model):
    __tablename__ = 'autor'

    autor_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    data_nascimento = db.Column(db.DateTime)

    def __init__(self, nome, data_nascimento):
        self.nome = nome
        self.data_nascimento = data_nascimento

    def serialize(self):
        return {
            'autor_id': self.autor_id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento
        }
    
    # Método para o GET (todos)
    @classmethod
    def list(cls):
        return cls.query.all()

    # Método para o GET
    @classmethod
    def retrieve(cls, id):
        return cls.query.filter_by(autor_id=id).first()

    # Método para o POST / UPDATE
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Método para o DELETE
    def delete(self):
        db.session.delete(self)
        db.session.commit()
```

E os métodos  no main.py:

```python
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
```

### Fazendo o vínculo dos livros e autores

Um livro normalmente é escrito por um autor, enquanto que um autor pode ter vários livros. Neste caso dizemos que 1 autor pode ter N livros, ou seja, temos um relacionamento 1:N (1 para N). Nesse caso, a tabela do livro armazenará o id do autor.

Através de SQL, este relacionamento acontece da seguinte forma:

```sql
--tabela livro
CREATE TABLE livro (
   livro_id INTEGER PRIMARY KEY,
   titulo VARCHAR(255),
   ano INTEGER
);

--tabela autor
CREATE TABLE autor (
   autor_id INTEGER PRIMARY KEY,
   nome VARCHAR(255),
   data_nascimento TIMESTAMP
);

-- relacionamento
ALTER TABLE livro ADD COLUMN autor_id INTEGER  --adiciona coluna
CONSTRAINT fk_livros_autores REFERENCES autor (autor_id)  --define como chave estrangeira para autor_id em autor
ON DELETE CASCADE; --se o autor for excluído, exclui o livro também
```

No Python, será necessário adicionar na classe Livro:

```python
autor_id = db.Column(db.Integer, db.ForeignKey('autor.autor_id'))
```

E também fazer as alterações nos métodos:

```python
    def __init__(self, titulo, ano, autor_id):
        self.titulo = titulo
        self.ano = ano
        self.autor_id = autor_id  # NOVO

    def serialize(self):
        return {
            'livro_id': self.livro_id,
            'titulo': self.titulo,
            'ano': self.ano,
            'autor_id': self.autor_id  # NOVO
        }
```

Será necessário adicionar na classe Autor:

```python
livros = db.relationship('Livro', backref='autor')
```

Agora, para cadastrar um livro vinculado com o autor, podemos alterar a request:

```python
requests.post(url='http://127.0.0.1:5000/livros', json={'titulo': 'Coraline', 'ano': 2020, 'autor_id': 1}, headers={'Content-type': 'application/json'})
```
