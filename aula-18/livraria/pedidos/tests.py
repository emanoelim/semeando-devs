from model_bakery import baker

from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from clientes.models import Cliente
from livros.models import Livro
from pedidos.models import Cupom, Pedido, PedidoLivro
from pedidos.views import PedidoView


class TestPedidoView(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.cliente = baker.make(Cliente)
        self.livro = baker.make(Livro)
        self.data = {
            'cliente': self.cliente.pk,
            'livros': [
                {
                    'livro': self.livro.pk,
                    'quantidade': 2
                }
            ],
            'cupom': 'app10'
        }

    def _post_request(self, data):
        request = self.factory.post('/pedidos/pedidos/', data, format='json')
        view = PedidoView.as_view({'post': 'create'})
        return view(request)
    
    def _put_request(self, data, pk):
        request = self.factory.put(f'/pedidos/pedidos/{pk}/', data, format='json')
        view = PedidoView.as_view({'put': 'update'})
        return view(request, pk=pk)
    
    def test_create_pedido_cupom_invalido(self):
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom inválido.'])

    def test_create_pedido_cupom_expirado(self):
        cupom = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom expirado.'])

    def test_update_pedido_mantendo_cupom(self):
        cupom_10 = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        cupom_20 = baker.make(Cupom, nome='APP20', quantidade_maxima=10, quantidade_utilizada=10)
        pedido = baker.make(Pedido, cliente=self.cliente, cupom=cupom_10)
        pedido_livro = baker.make(PedidoLivro, pedido=pedido, livro=self.livro, quantidade=2)
        resposta = self._put_request(self.data, pedido.pk)
        self.assertEqual(resposta.status_code, HTTP_200_OK)

    
    def test_update_pedido_alterando_para_cupom_expirado(self):
        cupom_10 = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        cupom_20 = baker.make(Cupom, nome='APP20', quantidade_maxima=10, quantidade_utilizada=10)
        pedido = baker.make(Pedido, cliente=self.cliente, cupom=cupom_10)
        pedido_livro = baker.make(PedidoLivro, pedido=pedido, livro=self.livro, quantidade=2)
        self.data['cupom'] = 'APP20' # troca o cupom dos dados para a chamada
        resposta = self._put_request(self.data, pedido.pk)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom expirado.'])

    def test_create_atualiza_quantidade_utilizada_do_cupom(self):
        cupom = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=0)
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.status_code, HTTP_201_CREATED)
        # recuperar cupom novamente para que a atualização seja refletida
        cupom = Cupom.objects.get(id=cupom.id)
        self.assertEqual(cupom.quantidade_utilizada, 1)

    def test_update_atualiza_quantidade_utilizada_do_cupom(self):
        cupom_10 = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=0)
        cupom_20 = baker.make(Cupom, nome='APP20', quantidade_maxima=10, quantidade_utilizada=0)
        pedido = baker.make(Pedido, cliente=self.cliente, cupom=cupom_10)
        pedido_livro = baker.make(PedidoLivro, pedido=pedido, livro=self.livro, quantidade=2)
        self.data['cupom'] = 'APP20' # troca o cupom dos dados para a chamada
        resposta = self._put_request(self.data, pedido.pk)
        self.assertEqual(resposta.status_code, HTTP_200_OK)
        # recuperar cupom novamente para que a atualização seja refletida
        cupom_20 = Cupom.objects.get(id=cupom_20.id)
        self.assertEqual(cupom_20.quantidade_utilizada, 1)


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