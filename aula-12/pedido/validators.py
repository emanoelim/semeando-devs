from livro.livros import Livro


def livro_valido(value, name):
    livro = Livro.retrieve(value)
    if not livro:
        raise ValueError('Livro id inválido.')
    return livro
