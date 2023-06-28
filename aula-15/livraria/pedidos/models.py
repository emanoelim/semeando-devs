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
    livros = models.ManyToManyField(Livro, through='PedidoLivro')
    cupom = models.ForeignKey(Cupom, null=True, blank=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        total = 0
        for livro in self.livros.all():
            # pedido_livro = PedidoLivro.objects.filter(pedido=self, livro=livro).first()
            pedido_livro = PedidoLivro.objects.get(pedido=self, livro=livro)
            valor = livro.valor
            quantidade = pedido_livro.quantidade
            total += valor * quantidade

        if self.cupom:
            desconto = total * self.cupom.percentual_desconto / 100
            if desconto > self.cupom.desconto_maximo:
                desconto = self.cupom.desconto_maximo
            total -= desconto

        return total


    def __str__(self):
        return f'{str(self.id)} - {self.cliente}'


class PedidoLivro(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
