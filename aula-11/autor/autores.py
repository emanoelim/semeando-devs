from db import db


class Autor(db.Model):
    __tablename__ = 'autor'

    autor_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    data_nascimento = db.Column(db.DateTime)
    livros = db.relationship('Livro', backref='autor')

    def __init__(self, nome, data_nascimento):
        self.nome = nome
        self.data_nascimento = data_nascimento

    def serialize(self):
        return {
            'autor_id': self.autor_id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.isoformat()
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
