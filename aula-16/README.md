# Aula 16

## Controle da quantidade de cupons

Normalmente as lojas oferecem uma quantidade máxima de cupons e após atingir esta quantidade, o cupom não funciona mais.
Vamos implmenntar esta lógica. Para isso vamos criar novos campos no Cupom:

```python
class Cupom(models.Model):
    nome = models.CharField(max_length=15)
    percentual_desconto = models.IntegerField()
    desconto_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_maxima = models.IntegerField(default=0)
    quantidade_utilizada = models.IntegerField(default=0)
```

Rodar o makemigrations e o migrate.

Vamos atualizar o validate_cupom() para retornar uma exceção caso a quantidade_maxima já tenha sido atingida:

```python
    def validate_cupom(self, value):
        value = value.upper()
        cupom = Cupom.objects.filter(nome=value).first()
        if not cupom:
            raise serializers.ValidationError('Cupom inválido.')
        
        if cupom.quantidade_utilizada >= cupom.quantidade_maxima:
            raise serializers.ValidationError('Cupom expirado.')
        
        return cupom
```

Vamos atualizar o create do pedido:

```python
    def create(self, validated_data):
        livros = validated_data.pop('pedidolivro_set')
        instance = Pedido.objects.create(**validated_data)
        for livro in livros:
            PedidoLivro.objects.create(pedido=instance, livro=livro['livro'], quantidade=livro['quantidade'])
        instance.total = instance.calcular_total()
        instance.save()

        # atualizar quantidade_utilizada no cupom
        cupom = validated_data.get('cupom')
        if cupom:
            cupom.quantidade_utilizada += 1
            cupom.save()

        return instance
```

Agora vamos atualizar a quantidade_maxima do cupom APP10 para 3. Após criar 3 pedidos com este cupom devemos ver a quantidade_utilizada igual 3. Após tentar adicionar um quarto pedido com o cupom, devemos ter um erro:

```json
{
  "cupom": [
    "Cupom expirado."
  ]
}
```

Vamos fazer um tratamento semelhante no update, porém a validação do cupom tem que ser antes de salvar a instance, pois nesse ponto a instance ainda tem os dados antigos, então conseguimos comparar o cupom antigo com o atual.

```python
    def update(self, instance, validated_data):
        livros = validated_data.pop('pedidolivro_set')
        instance.livros.clear()
        for livro in livros:
            PedidoLivro.objects.create(pedido=instance, livro=livro['livro'], quantidade=livro['quantidade'])
        
        cupom = validated_data.get('cupom')
        if cupom and cupom != instance.cupom:
            cupom.quantidade_utilizada += 1
            cupom.save()
        
        instance = super().update(instance, validated_data)
        instance.total = instance.calcular_total()
        instance.save()
        return instance
```

Caso de teste:
- Atualizar a quantidade_maxima do cupom APP10 para 4. 
- Criar um novo cupom, APP20.
- Criar um pedido que utiliza o APP20. Sua quantidade_utilizada será incrementada para 1. 
- Atualizar o pedido para utilizar o APP10. Agora a quantidade_utilizada do APP10 deve ser incrementada para 4.


## Testes automatizados

Cada vez que alteramos uma lógica precisamos testar novamente a aplicação. Ao fazer a lógica de atualizar a quantidade de cupons, tivemos que fazer vários passos:
- Atualizar a quantidade_maxima do cupom via admin;
- Criar novo cupom via admin;
- Cadastrar novo pedido via API;
- Atualzar novo pedido via API.

Todo o tempo gasto com estes testes manuais pode ser poupado utilizando testes automatizados.

Além disso, quando escrevemos um teste, é como se tivéssemos um "gabarito". Ao chamar uma função, sabemos que quantidade_utilizada deve ser atualizada para 3. Então escrevemos um teste para validar se o resultado que sai da função é realmente 3. 

Caso alguém altere esta função e ela passe a retornar 4, o teste irá falhar e a pessoa irá perceber que alterou o comportamente esperado da função, possivelmente causando um bug. Ou seja, os testes também ajudam a deixar a aplicação menos suscetível a bugs.

Os testes também vão evidenciar a importância de criar funções com apenas uma responsabilidade, pois testar uma função que faz diversas coisas diferentes se torna difícil, já uma função que faz apenas uma coisa é fácil de testar. 

Dentro da pasta de cada app já existe um arquivo chamado tests.py que criado automaticamente pelo Django. Todos os arquivos que começam com o prefixo "test" serão testados ao rodar o comando `python manage.py test`. Por enquanto, esta será a resposta:

```different
Found 0 test(s).
System check identified no issues (0 silenced).

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
```

Vamos iniciar criando testes para o package utils, pois nele teremos os testes mais simples. Como ele não foi criado pelo comando startapp, ele ainda não tem um tests.py, terá que ser criado o arquivo manualmente. 

Após isso, vamos criar uma classe de teste. Ela herda de TestCase, uma classe do Django que contém funções para facilitar os testes. A função setUp() é executada antes de cada teste. Dentro dela podemos declarar variáveis que serão de uso comum entre diversos testes em vez de criar elas repetidamente dentro de cada teste. Por enquanto vamos deixá-la vazia e conforme surgir a necessidade dessas variáveis, vamos atualizando.

```python
from django.test import TestCase


class TestUtils(TestCase):
    def setUp(self):
        pass
```

Os nome de cada teste também deve começar com o prefixo "test". Vamos escrever o primeiro para _retorna_digitos(), primeira função no arquivo:

```python
    ...
    def test_retorna_digitos(self):
        cpf = '123.456.789-10'
        digitos_cpf = _retorna_digitos(cpf)
        self.assertEqual(digitos_cpf, '12345678910')
```

Primeiro criamos a "entrada" do teste, o cpf. Depois chamamos a função desenvolvida, _retorna_digitos(), utilizando a entrada como parâmetro. Por fim, validamos se a saída da função corresponde com nosso "gabarito". 

Ao rodar o comando `python manage.py test` novamente, o resultado será:

```different
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.068s

OK
Destroying test database for alias 'default'...
```

Vamos propositalmente alterar a lógica da função _retorna_digitos():

```python
def _retorna_digitos(texto):
    if not texto or not isinstance(texto, str):
        return None
    return ' '.join([c for c in texto if c.isdigit()])  # adicionado espaço entre as as aspas.
```

Agora vamos rodar o comando `python manage.py test` novamente:

```different
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.F
======================================================================
FAIL: test_retorna_digitos (utils.tests.TestPedido.test_retorna_digitos)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/developer/Projetos/semeando-devs/aula-16/livraria/utils/tests.py", line 12, in test_retorna_digitos
    self.assertEqual(digitos_cpf, '12345678910')
AssertionError: '1 2 3 4 5 6 7 8 9 1 0' != '12345678910'
- 1 2 3 4 5 6 7 8 9 1 0
+ 12345678910


----------------------------------------------------------------------
Ran 2 tests in 0.066s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

A mensagem é bem clara: "FAIL: test_retorna_digitos (utils.tests.TestPedido.test_retorna_digitos), indicando que o teste falhou. Logo abaixo também vamos ter: "FAIL: test_retorna_digitos (utils.tests.TestPedido.test_retorna_digitos)" que compara o resultado obtido pela função _retorna_digitos() com o resultado esperado. 

Desta forma, se uma função estiver devidamente testada, qualquer alteração inadequada feita nela será detectada ao rodar os testes.

Vamos voltar a função ao normal para que o teste continue passando. 

Vamos criar dois testes para a função valida_cpf(). Ela tem dois tipos possíveis de retorno: True, se o cpf for válido ou False, se for inválido. Vamos testar os dois casos.

```python
    def test_retorna_cpf_valido(self):
        cpf_valido = '342.488.170-80'
        valido = valida_cpf(cpf_valido)
        self.assertTrue(valido)

    def test_retorna_cpf_invalido(self):
        cpf_invalido = '342.488.170-81'  # último dígito deveria ser 0
        valido = valida_cpf(cpf_invalido)
        self.assertFalse(valido)
```

Os testes devem continuar passando com estes dois novos testes. As funções de assert utilizadas são diferentes do primeiro teste, pois como o resultado de valida_cpf() é True ou False, podemos usar o assertTrue para validar se o resultado foi True ou o assertFalse para validar se o resultado foi False. 

ATIVIDADE: implementar o teste para mascara_cpf().

## Testes envolvendo objetos do banco

O próximo teste será para a função calcular_total(), do model Pedido. Este teste será um pouco mais avançado porque ele precisa de uma instância do Cliente e do Livro. Além disso, Livro precisa de um Autor.

Ao rodar os testes você deve ter percebido, bem no final, a mensagem: "Destroying test database for alias 'default'...". Ela aparece porque ao rodar os testes o Django cria um banco temporário exclusivo para testes. Todas as migrations do projeto são rodadas como se tívessemos feito um `python manage.py migrate`, então todas as tabelas vão exitir normalmente neste banco temporário. Porém, este banco estará sem dados, exceto pelos dados criados por padrão pelo Django. Sendo assim, teremos que criar alguns dados ao escrever os testes.

Outra coisa interessantes dos testes, é que devido a este fato de rodarem as migrations, eles também ajudam a pegar migrations inconsistentes.

Após finalizar a execução dos teste, o Django imediatamente apaga o banco de teste.

Para facilitar a criação dos dados durante os testes, vamos usar a biblioteca Model Bakery: https://model-bakery.readthedocs.io/en/latest/basic_usage.html.

Uma grande vantagem de utilizar esta biblioteca já é descrita na sua documentação. Ela traz um model exemplo:

```python
class Customer(models.Model):
    """
    Model class Customer of shop app
    """
    enjoy_jards_macale = models.BooleanField()
    name = models.CharField(max_length=30)
    email = models.EmailField()
    age = models.IntegerField()
    bio = models.TextField()
    days_since_last_login = models.BigIntegerField()
    birthday = models.DateField()
    last_shopping = models.DateTimeField()
```

Todos os campos do model são obrigatórios, então ao fazer um "customer = Customer.objects.create(), teríamos que passar os valores de todos os campos para não ter erro.

Com a biblioteca, basta fazer:

```python
customer = baker.make(Customer)
```

Ela irá criar todos os campos com valores aletários que correspondem aos tipos especificados no model.

Caso seja desejável especificar algum valor não aleatório, podemos passar ele por parâmetro normalmente, por exemplo:

```python
customer = baker.make(Customer, name='Fulano')
```

O objeto será criado com o name Fulano e todos os outros campos serão gerados aleatóriamente.

Chamamos isso de "mockar" dados.

A biblioteca também oferece outras vantagens para outros tipos de testes, vamos ver conforme a necessidade.

Vamos iniciar o teste, mockando alguns dados que poderão ser usado em diversos testes, por isso vamos fazer isso no setUp():

```python
class TestPedido(TestCase):
    def setUp(self):
        self.cliente = baker.make(Cliente)
        self.livro_1 = baker.make(Livro, valor=10)
        self.livro_2 = baker.make(Livro, valor=20)
        self.cupom = baker.make(Cupom, percentual_desconto=10, desconto_maximo=10)
        self.pedido = baker.make(Pedido)
```

Os valores dos livros e também do cupom foram especificados em vez de serem gerados aleatóriamente. Desta forma conseguimos calcular qual deve ser o resultado esperado ao chamar a função com os livros e o cupom mockados.

O primeiro teste será referente a um pedido sem cupom:

```python
    def test_calcular_total_pedido_sem_cupom_igual_40(self):  
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_1, quantidade=2)
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_2, quantidade=1)
        total = self.pedido.calcular_total()
        self.assertEqual(total, 40)
```

Neste teste adicionamos os livros ao pedido, juntamente com suas quantidades. Sendo 2 livros de valor 10 e um livro de valor 20, o total deve ser 40, visto que não há cupom. O nome do teste é bem específico e não tem problema. É melhor ter um nome de teste grande, mas que explique exatamente qual o seu propósito.

Vamos testar os mesmos dados acima, mas com cupom:

```python
    def test_calcular_total_pedido_com_cupom_igual_36(self):  
        self.pedido.cupom = self.cupom
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_1, quantidade=2)
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_2, quantidade=1)
        total = self.pedido.calcular_total()
        self.assertEqual(total, 36)
```

Sendo o cupom de 10%, o valor cai para 36.

Agora vamos aumentar a quantidade de itens para que a compra totalizasse 100 reais. Como o cupom é de 10% com desconto máximo de 10 reais, o valor do pedido deve ficar em 90 reais:

```python
    def test_calcular_total_pedido_com_cupom_igual_90(self):  
        self.pedido.cupom = self.cupom
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_1, quantidade=4)
        baker.make(PedidoLivro, pedido=self.pedido, livro=self.livro_2, quantidade=3)
        total = self.pedido.calcular_total()
        self.assertEqual(total, 90)
```

## Teste com exception

Outra parte do código onde desenvolvemos lógica foi no model Cliente. Lá existe um validdator que caso o cpf seja válido, aplica uma máscara e caso seja inválido retorna uma exception.

Primeiro vamos testar o caso do cpf válido:

```python
class TestValidatorsCliente(TestCase):
    def setUp(self):
        pass

    def test_valida_cpf_valido(self):
        cpf_sem_mascara = '34248817080'
        cpf_mascarado = validator_cpf(cpf_sem_mascara)
        self.assertEqual(cpf_mascarado, '342.488.170-80')
```

Quando a função dá uma exception, podemos testar da seguinte forma:

```python
    def test_valida_cpf_invalido(self):
        cpf_sem_mascara = '34248817081'  # último dígito deveria ser 0
        with self.assertRaises(ValidationError):
            validator_cpf(cpf_sem_mascara)
```

Todos os testes devem passar.

Para melhor entendimento, altere de:

```python
        with self.assertRaises(ValidationError):  
```

para:

```python
        with self.assertRaises(ValueError):
```

Agora o teste test_valida_cpf_invalido deve falhar:

```different
ERROR: test_valida_cpf_invalido (clientes.tests.TestValidatorsCliente.test_valida_cpf_invalido)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/developer/Projetos/semeando-devs/aula-16/livraria/clientes/tests.py", line 19, in test_valida_cpf_invalido
    validator_cpf(cpf_sem_mascara)
  File "/home/developer/Projetos/semeando-devs/aula-16/livraria/clientes/models.py", line 9, in validator_cpf
    raise ValidationError('CPF inválido.')
django.core.exceptions.ValidationError: ['CPF inválido.']
```

Pois o teste no teste estava previsto a exception ValidationError e não ValueError.

## Próxima aula

Ainda não fizemos os testes para as lógicas do serializer. Vamos ver isto na próxima aula, ao fazer testes para os endpoints da API.