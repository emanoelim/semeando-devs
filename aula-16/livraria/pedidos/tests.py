from model_bakery import baker

from django.test import TestCase

from clientes.models import Cliente
from livros.models import Livro
from pedidos.models import Cupom, Pedido, PedidoLivro


class TestPedido(TestCase):
    def setUp(self):
        self.cliente = baker.make(Cliente)
        self.livro_1 = baker.make(Livro, valor=10)
        self.livro_2 = baker.make(Livro, valor=20)
        self.cupom = baker.make(Cupom, percentual_desconto=10, desconto_maximo=10)
        self.pedido = baker.make(Pedido)

    def test_calcular_total_pedido_sem_cupom_igual_40(self):  
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_1, quantidade=2)
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_2, quantidade=1)
        total = self.pedido.calcular_total()
        self.assertEqual(total, 40)

    def test_calcular_total_pedido_com_cupom_igual_36(self):  
        self.pedido.cupom = self.cupom
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_1, quantidade=2)
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_2, quantidade=1)
        total = self.pedido.calcular_total()
        self.assertEqual(total, 36)

    def test_calcular_total_pedido_com_cupom_igual_90(self):  
        self.pedido.cupom = self.cupom
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_1, quantidade=4)
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_2, quantidade=3)
        total = self.pedido.calcular_total()
        self.assertEqual(total, 90)