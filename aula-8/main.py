from flask import Flask, request, jsonify
from musicas import Playlist


# cria uma intância de uma aplicação flask com o nome do modulo atual
app = Flask(__name__)

# http://127.0.0.1:5000/ 
@app.route('/')
def hello():
    return 'Hello, World!'

# http://127.0.0.1:5000/musicas
@app.route('/musicas', methods=['GET', 'POST'])
def musicas():
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

# http://127.0.0.1:5000/musicas/<id>
@app.route('/musicas/<id>', methods=['GET', 'PUT', 'DELETE'])
def musicas_id(id):
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


if __name__ == '__main__':
    playlist = Playlist()
    playlist.adiciona_musica('burning out', 'bad omens')
    playlist.adiciona_musica('traced in constellations', 'sleepmakewaves')
    playlist.adiciona_musica('venger', 'perturbator')
    app.run()
