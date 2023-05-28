from db import db


class Livro(db.Model):
    __tablename__ = 'livro'

    livro_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    ano = db.Column(db.Integer)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.autor_id'))

    def __init__(self, titulo, ano, autor_id):
        self.titulo = titulo
        self.ano = ano
        self.autor_id = autor_id

    def serialize(self):
        return {
            'livro_id': self.livro_id,
            'titulo': self.titulo,
            'ano': self.ano,
            'autor_id': self.autor_id
        }
    
    # Método para o GET (todos)
    @classmethod
    def list(cls):
        return cls.query.all()

    # Método para o GET
    @classmethod
    def retrieve(cls, id):
        return cls.query.filter_by(livro_id=id).first()

    # Método para o POST / UPDATE
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Método para o DELETE
    def delete(self):
        db.session.delete(self)
        db.session.commit()
