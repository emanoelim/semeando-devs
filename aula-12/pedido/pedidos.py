from db import db
from cliente.clientes import Cliente


livro_pedido = db.Table(
    'livro_pedido',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.pedido_id')),
    db.Column('livro_id', db.Integer, db.ForeignKey('livro.livro_id'))
)


class Pedido(db.Model):
    __tablename__ = 'pedido'

    pedido_id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.cliente_id'))
    data = db.Column(db.DateTime)
    livros = db.relationship('Livro', secondary=livro_pedido, backref='pedidos')

    def __init__(self, cliente_id, data):
        self.cliente_id = cliente_id
        self.data = data


    def serialize(self):
        cliente = Cliente.retrieve(self.cliente_id)
        dados_cliente = cliente.serialize() if cliente else None
        dados_livros = [livro.serialize() for livro in self.livros]
        return {
            'pedido_id': self.pedido_id,
            'cliente': dados_cliente,
            'data': self.data.isoformat(),
            'livros': dados_livros
        }
     
    # Método para o GET (todos)
    @classmethod
    def list(cls):
        return cls.query.all()

    # Método para o GET
    @classmethod
    def retrieve(cls, id):
        return cls.query.filter_by(pedido_id=id).first()

    # Método para o POST / UPDATE
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Método para o DELETE
    def delete(self):
        db.session.delete(self)
        db.session.commit()
