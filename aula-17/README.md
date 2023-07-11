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

O método _post_request() irá simular a chamada do endpoint POST .../pedidos/pedidos/. Na linha "view = PedidoView.as_view({'post': 'create'})" o dicionário faz o mapeamento do método http com o nome da função que deve ser chamada para ele.

O método _put_request() irá simular a chamada do endpoint PUT .../pedidos/pedidos/. Ele recebe também um parâmetro "pk" que será passado na url e também chamado na função view.

O primeiro teste utiliza um cupom que não existe e deve retorar um erro 400, junto com uma mensagem de cupom inexistente:

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

O segundo teste utiliza um cupom existente, mas que já está expirado:

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

Cliente, livro e data repetem nos dois testes e podem ser adicionados no setUp():

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

## Cadastro de endereço

Vamos iniciar criando uma tabela de endereço para o cliente:

```python
class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.IntegerField()
    cidade = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.cliente.nome}'
```

Os campos rua, cidade e uf foram deixados como null=True, pois a ideia é buscá-los automaticamente em uma API em vez de pedir para o usuário.

Depois adicionar no admin e rodar o makemigrations e o migrate:

```python
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'cidade', 'uf')
```

Vamos criar o serializer e a view:

```python
from rest_framework import serializers
from rest_framework import viewsets

from clientes.models import Cliente, Endereco


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nome', 'cpf', 'data_nascimento', 'email')


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'cliente', 'cep', 'rua', 'numero', 'cidade', 'uf')
        # Campos que serão adicionados automaticamente
        read_only_fields = ('rua', 'cidade', 'uf')


class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all() 
    serializer_class = ClienteSerializer 
    http_method_names = ['get', 'post', 'put', 'delete']  


class EnderecoView(viewsets.ModelViewSet):
    queryset = Endereco.objects.all() 
    serializer_class = EnderecoSerializer 
    http_method_names = ['get', 'post', 'put', 'delete']  
```

Também será necessário adicionar a view nas urls:

```python
from django.urls import path, include
from rest_framework import routers

from clientes.views import ClienteView, EnderecoView


router = routers.DefaultRouter()
router.register('clientes', ClienteView)
router.register('enderecos', EnderecoView)

urlpatterns = [
    path('clientes/', include(router.urls)),
]
```

Já deve ser possível cadastrar endereços pelo swagger.

## Service para consulta de CEP

Vamos criar um package "services", contendo um arquivo __ init __.py. Também vamos criar um arquivo
chamado cep_service.py. Neste arquivo vamos criar a classe CepService:

```python
import json
import requests


class CepService:
    def __init__(self):
        self.url = 'https://viacep.com.br/ws'

    def consultar_cep(self, cep):
        url = f'{self.url}/{cep}/json/'
        resposta = requests.get(url)
        resposta_json = json.loads(resposta.text)
        return resposta_json
```

Será necessário instalar a biblioteca requests e adicionar no requirements.txt (pip freeze > requirements.txt). 

Na função init é definida a url da API ViaCep (https://viacep.com.br/), que é uma API gratuita para consulta de CEPs.

A função consultar_cep faz a chamada da API passando um cep e converte a resposta para um json.

## Testando o service

Para testar se a API está sendo chamada com sucesso podemos criar um arquivo tests.py no package services e escrever a classe de teste abaixo:

```python
from django.test import TestCase

from services.cep_service import CepService


class TestCepService(TestCase):
    def setUp(self) -> None:
        self.service = CepService()

    def test_consultar_cep(self):
        reposta = self.service.consultar_cep('01001000')
        self.assertEqual(reposta.get('cep'), '01001-000')
```

O teste simplesmente chama a função que consulta o cep e valida se o cep que chega é igual ao retorno esperado da API, que pode ser encontrado em sua documentação:

```json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "complemento": "lado ímpar",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP",
  "ibge": "3550308",
  "gia": "1004",
  "ddd": "11",
  "siafi": "7107"
}
```

Então o teste verifica se a resposta está retornando o cep de acordo.

Agora que já verificamos que a função funciona corretamente, vamos marcar o teste com um decorator para que ele seja pulado quando formos rodar os testes, evitando chamadas desnecessárias para a API.


```python
from unittest import skip

from django.test import TestCase

from services.cep_service import CepService


class TestCepService(TestCase):
    def setUp(self) -> None:
        self.service = CepService()

    @skip('Acessa a API')
    def test_consultar_cep(self):
        reposta = self.service.consultar_cep('01001000')
        self.assertEqual(reposta.get('cep'), '01001-000')
```

## Utilizando o service para preencher o endereço

No model do Pedido, sobreescrevemos o create e o update do serializer, sendo que cada um teve uma lógica específica. Para o Endereceo, tanto o create quanto o update podem ter o mesmo comportamento, que é pegar o cep informado e extrair os dados faltantes a partir dele: rua, cidade e uf.

Sendo assim vamos separar esta lógica em um método para ser reaproveitado. Ele será criado no model Endereco:

```python
    def preencher_endereco(self):
        service = CepService()
        try:
            endereco = service.consultar_cep(self.cep)
            self.rua = endereco.get('logradouro')
            self.cidade = endereco.get('localidade')
            self.uf = endereco.get('uf')
        except Exception:
            pass
        self.save()
```

Agora basta sobreescrever o create e update para chamá-lo:

```python
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'cliente', 'cep', 'rua', 'numero', 'cidade', 'uf')
        read_only_fields = ('rua', 'cidade', 'uf')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.preencher_endereco()
        return instance
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.preencher_endereco()
        return instance   
```

Desta forma, ao chamar o POST ou PUT do endereço com os dados abaixo, por exemplo: 

```json
{
  "cliente": 1,
  "cep": "01001000",
  "numero": 200
}
```

Teremos o retorno:

```json
{
  "id": 5,
  "cliente": 1,
  "cep": "01001000",
  "rua": "Praça da Sé",
  "numero": 200,
  "cidade": "São Paulo",
  "uf": "SP"
}
```

## Teste dos endpoints

Como sobreescrevemos as lógicas de create e update, podemos criar testes para validar se os dados do endereço realmente estão sendo preenchidos após um create ou update. A ideia será parecida com os testes de endpoints do PedidoView:

```python
class TestEnderecoView(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.cliente = baker.make(Cliente)
        self.data = {
            'cliente': self.cliente.id,
            'cep': '01001000',
            'numero': 200
        }

    def _post_request(self, data):
        request = self.factory.post('/clientes/enderecos/', data, format='json')
        view = EnderecoView.as_view({'post': 'create'})
        return view(request)
    
    def _put_request(self, data, pk):
        request = self.factory.put(f'/clientes/enderecos/', data, format='json')
        view = EnderecoView.as_view({'put': 'update'})
        return view(request, pk=pk)

    def test_endereco_preenchido_create(self):
        pass

    def test_endereco_preenchido_update(self):
        pass
```

Teste test_endereco_preenchido_create:

```python
    def test_endereco_preenchido_create(self):
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.data['rua'], 'Praça da Sé')
        self.assertEqual(resposta.data['cidade'], 'São Paulo')
        self.assertEqual(resposta.data['uf'], 'SP')
```

Teste test_endereco_preenchido_update (quase a mesma coisa, mas primeiro criamos o Endereco para poder atualizar):

```python
    def test_endereco_preenchido_update(self):
        endereco = baker.make(Endereco)
        resposta = self._put_request(self.data, endereco.id)
        self.assertEqual(resposta.data['rua'], 'Praça da Sé')
        self.assertEqual(resposta.data['cidade'], 'São Paulo')
        self.assertEqual(resposta.data['uf'], 'SP')
```

## Mock do Service

Estes testes acabam realmente chamando a API. Para evitar isso vamos fazer um mock do CepService no início do arquivo:

```python
mock_cep_service = {
    "cep": "01001-000",
    "logradouro": "Praça da Sé",
    "complemento": "lado ímpar",
    "bairro": "Sé",
    "localidade": "São Paulo",
    "uf": "SP",
    "ibge": "3550308",
    "gia": "1004",
    "ddd": "11",
    "siafi": "7107"
}
```

Vamos precisar do seguinte import:

```python
from unittest.mock import Mock, patch
```

Para poder usar o decorator nos testes:

```python
    @patch.object(CepService, 'consultar_cep', Mock(return_value=mock_cep_service))
    def test_endereco_preenchido_create(self):
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.data['rua'], 'Praça da Sé')
        self.assertEqual(resposta.data['cidade'], 'São Paulo')
        self.assertEqual(resposta.data['uf'], 'SP')

    @patch.object(CepService, 'consultar_cep', Mock(return_value=mock_cep_service))
    def test_endereco_preenchido_update(self):
        endereco = baker.make(Endereco)
        resposta = self._put_request(self.data, endereco.id)
        self.assertEqual(resposta.data['rua'], 'Praça da Sé')
        self.assertEqual(resposta.data['cidade'], 'São Paulo')
        self.assertEqual(resposta.data['uf'], 'SP')
```

Seus parâmetros são: uma classe, um método da classe o retorno esperado para o método. Ou seja, estamos definindo que o método consultar_cep do CepService deve retornar os dados que definimos no mock_cep_service. Isso signifca que no momento em que o código deveria chamar o método consultar_cep, ele não vai realmente chamar o método, ele simplesmente vai atribuir o que está em mock_cep_service ao resultado do método. 

Desta forma, evitamos chamadas desncessárias para API e como o mock_cep_service simula um retorno real dela, ainda conseguimos testar o comportamento de preencher os dados faltantes do endereço ao salvar/atualizar.

Este tipo de teste pode ser chamado sempre que precisarmos testar algum endpoint ou mesmo alguma função que precise acessar um serviço externo. Muitas vezes estes serviços são pagos, além de os testes ficaram mais demorados por estarem fazendo chamadas externas.

## Atividade

### Endereço

- Criar uma função valida_cep que valida se uma string é um cep composto por 8 números.
- Criar testes para a função.
- Utilizar a função no serializer para evitar o cadastro com ceps inválidos.
- Criar um teste de endpoint para verificar se o endpoint está retornando um erro 400 e uma mensagem adequada para quando o endpoint for chamado com um cep inválido.

### Cliente

- Hoje o sistema está permitindo cadastrar clientes com cpfs repetidos, então adicionar no serializer (write, se houverem 2) uma validação para dar um erro quando o usuário tentar cadastrar um cpf que já existe.
- Criar os testes para o endpoint do cliente, testando as duas situações: cadastro com cpf novo, retornando sucesso e cadastro com cpf que já existe, retornando erro.
