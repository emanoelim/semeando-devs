from django.db import models

from clientes.models import Cliente
from livros.models import Livro


class Cupom(models.Model):
    nome = models.CharField(max_length=15)
    percentual_desconto = models.IntegerField()
    desconto_maximo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
    

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='clientes_pedido')
    data = models.DateTimeField(auto_now_add=True)
    livros = models.ManyToManyField(Livro, through='PedidoLivros')
    cupom = models.ForeignKey(Cupom, null=True, blank=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_total(self):
        total = 0
        for livro in self.livros.all():
            livro_pedido = PedidoLivros.objects.get(pedido=self, livro=livro)
            valor = livro.valor
            quantidade = livro_pedido.quantidade
            total += valor * quantidade

        if self.cupom:
            desconto = total * self.cupom.percentual_desconto / 100
            if desconto > self.cupom.desconto_maximo:
                desconto = self.cupom.desconto_maximo
            total -= desconto

        self.total = total
        self.save()
        return self

    def __str__(self):
        return f'{str(self.id)} - {self.cliente}'


class PedidoLivros(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.pedido} - {self.livro} ({self.quantidade})'
