# Aula 17

## Testando os endpoints

No arquivo tests.py do pedidos, adicionar o import:

```python
from rest_framework.test import APITestCase, APIRequestFactory
```

Criar a classe de teste para o PedidoView:

```python
class TestPedidoView(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def _post_request(self, data):
        request = self.factory.post('/pedidos/pedidos/', data, format='json')
        view = PedidoView.as_view({'post': 'create'})
        return view(request)
    
    def _put_request(self, data, pk):
        request = self.factory.put(f'/pedidos/pedidos/{pk}/', data, format='json')
        view = PedidoView.as_view({'put': 'update'})
        return view(request, pk=pk)
```

O método _post_request() irá simular a chamada do endpoint POST .../pedidos/pedidos/. Na linha "view = PedidoView.as_view({'post': 'create'})" o dicionário faz o mapeamento do método http com o nome da função que deve ser chamada para o ele.

O método _put_request() irá simular a chamada do endpoint PUT .../pedidos/pedidos/. Ele recebe também um parâmetro "pk" que será passado na url e também chamado na função view.

O primeiro teste utiliza um cupom não existe e deve retorar um erro 400, junto com uma mensagem de cupom inexistente:

```python
    def test_create_pedido_cupom_invalido(self):
        cliente = baker.make(Cliente)
        livro = baker.make(Livro)
        data = {
            'cliente': cliente.pk,
            'livros': [
                {
                    'livro': livro.pk,
                    'quantidade': 2
                }
            ],
            'cupom': 'app10'
        }
        resposta = self._post_request(data)  # executa a chamada ao endpoint passando os dados acima
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom inválido.'])
```

O segundo teste utiliza um cupom existem, mas que já está expirado:

```python
    def test_create_pedido_cupom_expirado(self):
        cliente = baker.make(Cliente)
        livro = baker.make(Livro)
        cupom = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        data = {
            'cliente': cliente.pk,
            'livros': [
                {
                    'livro': livro.pk,
                    'quantidade': 2
                }
            ],
            'cupom': 'app10'
        }
        resposta = self._post_request(data)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom expirado.'])
```

cliente, livro e data repetem nos dois testes e podem ser adicionados no setUp():

```python
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

    ...

    def test_create_pedido_cupom_invalido(self):
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom inválido.'])

    def test_create_pedido_cupom_expirado(self):
        cupom = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom expirado.'])
```

Uma lógica desenvolvida no validate_cupom() é para quando for uma atualização:
- Ao manter o mesmo cupom, não é necessário validar se o cupom está expirado;
- Se for alterado o cupom, deve validar se o cupom está expirado:

```python
    def validate_cupom(self, value):
        value = value.upper()
        cupom = Cupom.objects.filter(nome=value).first()
        if not cupom:
            raise serializers.ValidationError('Cupom inválido.')
        
        # quando é atualização existe um self.instance, quando é criação fica None
        if not self.instance or self.instance.cupom != cupom:
            if cupom.quantidade_utilizada >= cupom.quantidade_maxima:
                raise serializers.ValidationError('Cupom expirado.')
        
        return cupom
```

Então estas duas situações podem ser testadas:

```python
    def test_update_pedido_mantendo_cupom(self):
        cupom_10 = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        cupom_20 = baker.make(Cupom, nome='APP20', quantidade_maxima=10, quantidade_utilizada=10)
        pedido = baker.make(Pedido, cliente=self.cliente, cupom=cupom_10)
        pedido_livro = baker.make(PedidoLivro, pedido=pedido, livro=self.livro, quantidade=2)
        # dados enviados
        # {
        #     'cliente': self.cliente.pk,
        #     'livros': [
        #         {
        #             'livro': self.livro.pk,
        #             'quantidade': 2
        #         }
        #     ],
        #     'cupom': 'app10'
        # }
        resposta = self._put_request(self.data, pedido.pk)
        self.assertEqual(resposta.status_code, HTTP_200_OK)

    def test_update_pedido_alterando_para_cupom_expirado(self):
        cupom_10 = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=10)
        cupom_20 = baker.make(Cupom, nome='APP20', quantidade_maxima=10, quantidade_utilizada=10)
        pedido = baker.make(Pedido, cliente=self.cliente, cupom=cupom_10)
        pedido_livro = baker.make(PedidoLivro, pedido=pedido, livro=self.livro, quantidade=2)
        self.data['cupom'] = 'app20' # troca o cupom dos dados para a chamada
        # dados enviados
        # {
        #     'cliente': self.cliente.pk,
        #     'livros': [
        #         {
        #             'livro': self.livro.pk,
        #             'quantidade': 2
        #         }
        #     ],
        #     'cupom': 'app20'
        # }
        resposta = self._put_request(self.data, pedido.pk)
        self.assertEqual(resposta.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['cupom'], ['Cupom expirado.'])
```

Como é um update, tivemos que criar um pedido (e consequentemente um pedido_livro) para poder chamar o update em relação a este pedido. Também criamos dois cupons, o cupom_10, que é o cupom que está no pedido, e o cupom_20, que vai ser enviado na request no segundo teste, para simular a troca de cupom.

Outra lógia que pode ser testada é a atualização da quantidade_utilizada do cupom:

```python
    def test_create_atualiza_quantidade_utilizada_do_cupom(self):
        cupom = baker.make(Cupom, nome='APP10', quantidade_maxima=10, quantidade_utilizada=0)
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.status_code, HTTP_201_CREATED)
        # recuperar cupom novamente para que a atualização seja refletida
        cupom = Cupom.objects.get(id=cupom.id)
        self.assertEqual(cupom.quantidade_utilizada, 1)
```

E também para o update:

```python
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
```

