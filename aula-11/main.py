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