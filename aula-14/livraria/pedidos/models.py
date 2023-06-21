from django.db import models

from clientes.models import Cliente
from livros.models import Livro


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='clientes_pedido')
    data = models.DateTimeField(auto_now_add=True)
    livros = models.ManyToManyField(Livro)

    def __str__(self):
        return f'{str(self.id)} - {self.cliente}'


# class PedidoLivro(models.Model):
#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
#     livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
#     quantidade = models.IntegerField(default=1)

