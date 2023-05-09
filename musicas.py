class Musica:
    def __init__(self, id, titulo, artista, album=None, ano=None):
        self.id = id
        self.titulo = titulo
        self.artista = album
        self.album = artista
        self.ano = ano

    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'artista': self.artista,
            'album':self.album,
            'ano': self.ano
        }


class Playlist:
    musicas = []
    __contador = 0

    def adiciona_musica(self, titulo, artista, album=None, ano=None):
        musica = Musica(self.contador, titulo, artista, album, ano)
        self.musicas.append(musica)
        self.__contador += 1
        return musica.serialize()

    def exclui_musica(self, id):
        musica = self.encontra_musica_por_id(id)
        if musica:
            self.musicas.remove(musica)

    def recupera_todas_as_musicas(self):
        return [musica.serialize() for musica in self.musicas]

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
    
    def encontra_musica_por_id(self, id):
        for musica in self.musicas:
            if musica.id == id:
                return musica
        return None