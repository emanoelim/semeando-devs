# semeando-devs-flask

### Configurando o projeto
* Criar uma pasta chamada **flask**.
* Abrir um terminal na pasta criada.
* Criar uma virtualenv: `python -m venv .venv`.
* Ativar a venv: `.venv/bin/activate`
* Instalar a lib **flask**: `pip intall flask`.
* Instalar a lib **requests**, para testar as chamadas: `pip install requests`.

### Criando o primeiro endpoint
Na pasta flask criar um arquivo chamado **main.py**, com o conteúdo:

```python
from flask import Flask


# cria uma intância de uma aplicação flask com o nome do modulo atual
app = Flask(__name__)  

@app.route('/')
def hello():
    return 'Hello, World!'
```

Para rodar a aplicação, executar o comando: `flask --app main run`.

Também podemos fazer a seguinte modificação, para rodar com o comando `python -m main`.

```python
from flask import Flask


app = Flask(__name__)  

# cria uma intância de uma aplicação flask com o nome do modulo atual
@app.route('/')
def hello():
    return 'Hello, World!'
    
  
if __name__ == '__main__':
    app.run()
```

Ainda no terminal, deve aparecer uma mensagem do tipo:

```different
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Ao acessar a url http://127.0.0.1:5000 no navegador, você deve ver a mensagem **Hello, World!**.

127.0.0.1 é o endereço local do computador.

### Operações de CRUD
Normalmente uma API contém os endpoints para:
* POST - adicionar um objeto;
* PUT - atualizar um objeto;
* GET / GET id - recuperar todos os objetos / recuperar um objeto específico;
* DELETE - excluir um objeto.

Desta forma vamos criar algumas classes para representar um objeto e as operações acima. Isto será feito em um arquivo chamado **musicas.py** (no mesmo nível do main.py).

```python
class Musica:
    def __init__(self, id, titulo, artista, album=None, ano=None):
        self.id = id
        self.titulo = titulo
        self.artista = album
        self.album = artista
        self.ano = ano
        
        
class Playlist:
    musicas = []
    __contador = 0  # utilizado para gerar o identificador de cada música
```

Método da classe Playlist para adicionar uma música na playlist (será usado pelo POST):
```python
    def adiciona_musica(self, titulo, artista, album=None, ano=None):
        musica = Musica(self.__contador, titulo, artista, album, ano)
        self.musicas.append(musica)
        self.__contador += 1
        return musica
```

Por enquanto nada será salvo em banco. Os dados serão recriados a cada execução do programa.

Método para excluir uma música com um id específico (será usado pelo DELETE):

```python
    def exclui_musica(self, id):
        for musica in self.musicas:
            if musica.id == id:
                item = musica
        if item:
            self.musicas.remove(item)
```

Método para recuperar TODAS as músicas (será usado pelo GET):

```python
    def recupera_todas_as_musicas(self):
        return self.musicas
```

Método para recuperar UMA música com um id específico (será usado pelo GET id):

```python
    def recupera_musica(self, id):
        for musica in self.musicas:
            if musica.id == id:
                return self.musica
            return None
```

Método para atualizar uma música com um id específico (será usado pelo PUT):

```python
    def atualiza_musica(self, id, titulo, artista, album, ano):
        for musica in self.musicas:
            if musica.id == id:
                musica.titulo = titulo
                musica.artista = artista
                musica.album = album
                musica.ano = ano
                return musica
        return None
```

Uma API norlmalmente retorna os dados no formato JSON, sendo assim vamos criar um método na classe Musica que pega o objeto e converte para estse formato:

```python
    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'artista': self.artista,
            'album':self.album,
            'ano': self.ano
        }
```

Os métodos da playlist podem ser atualizados para ter o retorno adequado:

```python
    def adiciona_musica(self, titulo, artista, album=None, ano=None):
        musica = Musica(self.__contador, titulo, artista, album, ano)
        self.musicas.append(musica)
        self.__contador += 1
        return musica.serialize()

    def exclui_musica(self, id):
        for musica in self.musicas:
            if musica.id == id:
                item = musica
        if item:
            self.musicas.remove(item)

    def recupera_todas_as_musicas(self):
        return [musica.serialize() for musica in self.musicas]

    def recupera_musica(self, id):
        for musica in self.musicas:
            if musica.id == id:
                return musica.serialize()
        return None
    
    def atualiza_musica(self, id, titulo, artista, album, ano):
        for musica in self.musicas:
            if musica.id == id:
                musica.titulo = titulo
                musica.artista = artista
                musica.album = album
                musica.ano = ano
                return musica.serialize()
        return None
```

### Criando endpoint para o GET
No arquivo **main.py** adicionar a seguinte função após a função **hello()**:

```python
@app.route('/musicas', methods=['GET'])
def get_all():
    data = playlist.recupera_todas_as_musicas()
    resposta = {
        'data': data,
    }
    return resposta, 200
```

O valor 200 (OK) no return é o **status** da resposta e indica que houve sucesso.

Agora é possível acessar a url http://127.0.0.1:5000/musicas no navegador e ver todas as músicas da playlist.

### Criando endpoint para o GET id
Após a função acima, criar a função:

```python
@app.route('/musicas/<id>', methods=['GET'])
def get_id(id):
    data = playlist.recupera_musica(int(id))
    resposta = {
        'data': data,
    }
    return resposta, 200
```

Agora é possível acessar a url http://127.0.0.1:5000/musicas/1 no navegador e ver a música de id 1, por exemplo.

### Criando o endpoint para o POST
Neste caso, para que possamos utilizar a mesma url http://127.0.0.1:5000/musicas, apenas alternando o método HTTP, vamos atualizar o método **get_all()** para 
que diferencie qual método foi chamado e realize as instruções de acordo:

```python
@app.route('/musicas', methods=['GET', 'POST'])
def get_all():
    if request.method == 'GET':
        data = playlist.recupera_todas_as_musicas()
        resposta = {
            'data': data,
        }
        return resposta, 200
    
    else:
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        artista = request_data.get('artista')
        album = request_data.get('album')
        ano = request_data.get('ano')
        data = playlist.adiciona_musica(titulo, artista, album, ano)
        resposta = {
            'data': data,
        }
        return resposta, 201
```

O 201 (Created) é o status que indica que um objeto foi criado com sucesso.

Para testar esta chamada vamos utilizar o auxílio da lib requests:
* Abrir um terminal Python;
* Executar o coamndo: `import requests`.
* Executar o comando: `r = requests.post(url='http://127.0.0.1:5000/musicas', json={'titulo': 'lost', 'artista': 'linkin park'}, headers={'Content-type': 'application/json'})`.
* Para verificar se tudo deu certo, executar o comando: `r`. Assim, deve aparecer o status code da chamada como 201.
* Acessar a url http://127.0.0.1:5000/musicas no navegador e ver a playlist atualizada.

### Criando o endpoint para o PUT
Também será atualizado o endpoint **get_id()** para que a chamada também possa ficar em http://127.0.0.1:5000/musicas/id, apenas alternando o método HTTP.

```python
@app.route('/musicas/<id>', methods=['GET', 'PUT'])
def get_id(id):
    if request.method == 'GET':
        data = playlist.recupera_musica(int(id))
        resposta = {
            'data': data,
        }
        return resposta, 200
    
    else:
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        artista = request_data.get('artista')
        album = request_data.get('album')
        ano = request_data.get('ano')
        data = playlist.atualiza_musica(int(id), titulo, artista, album, ano)
        resposta = {
            'data': data,
        }
        return resposta, 200
```

Ainda no terminal Python, testar:
* `requests.put(url='http://127.0.0.1:5000/musicas/2', json={'titulo': 'bury it', 'artista': 'chvrches'}, headers={'Content-type': 'application/json'})`.
* `r` (deve apresentar o status code 200).
* Acessar a url http://127.0.0.1:5000/musicas no navegador e ver a playlist atualizada.

### Criando endpoint para o DELETE
Da mesma forma, será atualizado o **get_id()**:

```python
@app.route('/musicas/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_id(id):
    if request.method == 'GET':
        data = playlist.recupera_musica(int(id))
        resposta = {
            'data': data,
        }
        return resposta, 200
    
    elif request.method == 'PUT':
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        artista = request_data.get('artista')
        album = request_data.get('album')
        ano = request_data.get('ano')
        data = playlist.atualiza_musica(int(id), titulo, artista, album, ano)
        resposta = {
            'data': data,
        }
        return resposta, 200
    
    else:
        data = playlist.exclui_musica(int(id))
        resposta = {
            'data': data,
        }
        return resposta, 204
```

O status 204 (No content) indica que o objeto não existe mais:

Para testar:
* `requests.delete(url='http://127.0.0.1:5000/musicas/2')]`.
* `r` (deve retornar 204).

### Melhorias
Vamos criar um método **encontra_musica_por_id()** na classe Playlist, que poderá ser reaproveitado por diversos métodos:

```python
    def encontra_musica_por_id(self, id):
        for musica in self.musicas:
            if musica.id == id:
                return musica
        return None
```

Após esta alteração, as funções abaixo podem ser refatoradas, evitando repetição de código:

```python
    def exclui_musica(self, id):
        musica = self.encontra_musica_por_id(id)
        if musica:
            self.musicas.remove(musica)

    def recupera_musica(self, id):
        musica = self.encontra_musica_por_id(id)
        if musica:
            return musica.serialize()
        return None
    
    def atualiza_musica(self, id, titulo, artista, album, ano):
        musica = self.encontra_musica_por_id(id)
        if musica:
            musica.titulo = titulo
            musica.artista = artista
            musica.album = album
            musica.ano = ano
            return musica.serialize()
        return None
```

Também vamos aproveitar o método para atualizar os endpoints **musicas/id** para que já retornem um erro 404 (Not found) no caso de objeto informado não existir:

```python
 @app.route('/musicas/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_id(id):
    musica = playlist.encontra_musica_por_id(int(id))
    if not musica:
        resposta = {
            'data': [],
        }
        return resposta, 404
    
    if request.method == 'GET':
        data = playlist.recupera_musica(int(id))
        resposta = {
            'data': data,
        }
        return resposta, 200
    
    elif request.method == 'PUT':
        request_data = request.get_json()
        titulo = request_data.get('titulo')
        artista = request_data.get('artista')
        album = request_data.get('album')
        ano = request_data.get('ano')
        data = playlist.atualiza_musica(int(id), titulo, artista, album, ano)
        resposta = {
            'data': data,
        }
        return resposta, 200
    
    else:
        data = playlist.exclui_musica(int(id))
        resposta = {
            'data': data,
        }
        return resposta, 204
```

Podemos testar as operações com id novamente para verificar o retorno 404, basta informar ids que não existem.
* `requests.get(url='http://127.0.0.1:5000/musicas/20')]`.
* `requests.put(url='http://127.0.0.1:5000/musicas/20', json={'titulo': 'bury it', 'artista': 'chvrches'}, headers={'Content-type': 'application/json'})`.
* `requests.delete(url='http://127.0.0.1:5000/musicas/20')]`.

### Trabalhos futuros

Esta API foi feita de forma bem manual, para entendimento dos métodos HTTP. Futuramente, vamos utilizar algumas funcionalidades prontas para 
faciltiar o trabalho.

Também devem ser adicionadas validações antes de criar/atualizar um objeto, garantindo que os dados informados pelo usuário nas chamadas de POST/PUT estejam de
acordo com o esperado.













