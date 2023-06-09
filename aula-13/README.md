# Aula 13

## Django

É um framework open source, de alto nível, focado no desenvolvimento web com Python.

- https://www.djangoproject.com/.

Ele foi criado para ajudar o desenvolvedor a construir aplicações da maneira mais rápida possível.

Ele conta com uma comunidade muito ativa. É muito fácil encontrar tutoriais e bibliotecas que adicionam funcionalidades extra para o framework.

Neste tutorial oficial do Django é possível encontrar um passo a passo para construir uma aplicação: https://docs.djangoproject.com/en/4.2/intro/tutorial01/.

O Django vem com várias ferramentas para facilitar o desenvolvimento:

- ORM (Object Relational Mapper): da mesma maneira que o SQL Alchemy (biblioteca que instalamos no projeto Flask), o ORM do Django nos permite interagir com o banco de dados de maneira bem alto nível, utilizando classes, sem a necessidade de escrever SQL.

- Admin: uma interface que permite fazer o CRUD das tabelas do banco de dados, além de fazer cadastro e gerenciamento de usuários, entre outras possibilidades.

- Autenticação e autorização: o Django já implementa o cadastro de usuários e grupos de acesso. Cada vez que você cria uma nova tabela pelo Django, automaticamente são criadas permissões para criar, visualizar, atualizar e excluir aquele tipo de objeto. Desta forma, estas permissões podem ser vinculadas a usuários e grupos específicos que poderão acessar o objeto.

- Templates: o Django também permite criar páginas HTML que interagem facilmente com os objetos do backend, permitindo criar um "fronted" rapidamente para a aplicação.

- Testes: ferramentas para criar e executar testes automatizados.

## Django rest framework (DRF)

É uma biblioteca que facilita muito o desenvolvimento de APIs com Django (semelhante ao Flask-Restful para o Flask).

- https://www.django-rest-framework.org/.

## Projeto da livraria utilizando o Django

Nesta aula vamos estudar as funcionalidades do Django, replicando o mesmo projeto da livraria que fizemos com Flask.

### Criando o projeto

O primeiro passo é instalar o Django:

```different
python -m pip install Django
```

O comando irá instalar a versão mais recente do framework.

Depois, na pasta desejada, execute o comando para criar um novo projeto Django para a livraria:

```different
django-admin startproject livraria
```

A seguinte estrutura de arquivos será criada:

![estrutura-django](figuras/estrutura-django.png)

A pasta mais externa "livraria" é simplesmente a pasta que guarda o projeto e pode ser seu nome alterado se desejado.

A pasta mais interna "livraria" é o Python package do projeto (veja que contém o __ init __.py). Dentro dele teremos os arquivos:

- asgi.py: utilizado quando formos subir a aplicação em um servidor compatível com ASGI.

- settings.py: confgurações do projeto. Aqui vamos especificar idioma do projeto, variáveis do banco de dados (usuário, senha, etc), urls que poderão acessar a aplicação, entre outras configurações. 

- urls.py: mapeamento das urls, como faziamos no main.py do Flask. Aqui fica em um arquivo separado.

- wsgi.py: utilizado quando formos subir a aplicação em um servidor compatível com WSGI.

O manage.py é um arquivo que permite executar comandos para interagir com a aplicação como executar o projeto, executar testes, iniciar um terminal específico para interagir com o ORM, entre outros.

Com esta estrutura criada e estando dentro da pasta mais externa "livraria" nós podemos executar o comando para rodar a aplicação: `python manage.py runserver`.

Se tudo der certo ela deve ficar disponível na url http://127.0.0.1:8000/. Ao acessar a url você deve ver a mensagem: The install worked successfully! Congratulations!

### Criando um app
Um projeto é composto por vários apps. Normalmente um app é usado para reperesentar um domínio da aplicação. No caso da livraria podemos pensar em alguns domínios: 

- livros: incluindo as tabelas de livros, autores e editoras;

- clientes: incluindo tabelas de clientes, contatos e endereços;

- pedidos: tabelas de pedidos e cupons, por exemplo.

Para começar, vamos criar o app "livros": `python manage.py startapp livros`.

Também será necessário adicionar o novo app no settings.py. Já existem alguns apps cadastrados, que são apps padrão do Django:

```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'livros',  # novo app
]
...
```

O app vai ter a estrutura:

![estrutura-app](figuras/estrutura-app.png)

- migrations: quando criarmos ou alterarmos uma classe que representa uma tabela vamos precisar rodar um comando que irá gerar um arquivo de migration, que representará as operações que iremos fazer no banco de dados. Veremos mais detalhamente ao utilizar.

- admin.py: aqui poderemos registrar as tabelas criadas para que apareçam no painel do admin. Por enquanto estará vazio.

- apps.py: arquivo de configuração do app.

- models.py: aqui vamos criar as classes que representam as tabelas, como faziamos, por exemplo, no arquivo livros.py. Por enquanto estará vazio.

- tests.py: aqui podemos criar testes automatizados. Por enquanto está vazio. Será visto mais adiante.

- views.py: aqui serão criados os métodos de get, post, put e delete, semelhante ao que faziamos no resources.py. Por enquanto está vazio.

### Criado os models do app livro

No arquivo models.py:

```python
from django.db import models


# Flask
# class Livro(db.Model):
#     __tablename__ = 'livro'
#
#     livro_id = db.Column(db.Integer, primary_key=True)
#     titulo = db.Column(db.String(255))
#     ano = db.Column(db.Integer)
#     autor_id = db.Column(db.Integer, db.ForeignKey('autor.autor_id'))

class Livro(models.Model):
    # o id é gerado automaticamente
    titulo = models.CharField(max_length=255)
    ano = models.IntegerField()
    # autor_id será adicionado depois
```

### Registrando os models no admin

No arquivo admin.py:

```python
from django.contrib import admin

from livros.models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # campos que vão aparecer na listagem
    list_display = ('id', 'titulo', 'ano')
```

Depois de adicionar o app no settings.py e registrar a tabela no admin.py é necessário rodar o comando: `python manage.py makemigrations`.

Isso vai gerar automaticamente um novo arquivo no package migrations do app livros, chamado 0001_initial.py, com o conteúdo:

```python
# Generated by Django 4.1.7 on 2023-06-11 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('ano', models.IntegerField()),
            ],
        ),
    ]
```

É possível ver que mesmo não especificando o id no model.py ele é gerado automaticamente como uma primary key.

Neste ponto, as alterações em banco representadas neste arquivo ainda não foram aplicadas. Para que isso aconteça é necessário rodar o comando: `python manage.py migrate`.

Ao rodar este comando a tabela será criada no banco de dados. Como não configuramos nenhum banco até este momento, será usado o SQLite por padrão, que é o que já vem configurado no settings.py:

```python
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
...
```

Vamos executar o comando: `python manage.py createsuperuser`. 

Ele permite criar um usuário administrador para acessar o painel admin do Django, basta informar os dados solicitados: username, e-mail (não será enviado nenhum e-mail nesse por enquanto, pode ser qualquer um) e password. Para acessar o painel admin, acesar a url http://127.0.0.1:8000/admin, que irá redirecionar para a tela de login:

![admin](figuras/admin.png)

Após logar já é possível ver a tabela dos livros:

![livros-admin](figuras/livros-admin.png)

Clicando na tabela Livros, pelo botão "ADD LIVRO +" aparecerá um formulário para cadastrar um livro novo:

![novo-livro](figuras/novo-livro.png)

Os campos especificados no admin.py vão aparecer na listagem:

![listagem](figuras/listagem.png)

### Criando as views do app livro

Primeiramente vamos instalar a biblioteca Django rest framwork, que vai facilitar bastante a criação das views. Devemos rodar o comando: `pip install djangorestframework`.

Também será necessário adicionar o app do Django rest framework no settings.py:

```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # app do DRF
    'livros',
]
...
```

Antes de criar os métodos para os endpoints preciamos definir o serializer do livro (semelhante ao método serialize() da classe livro do projeto Flask). No Django ele não será um método, será uma classe. Vamos criá-lo em views.py:

```python
from rest_framework import serializers

from livros.models import Livro


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        # campos que queremos serializar
        fields = ('id', 'titulo', 'ano')
```

Com o serializer criado já é possível criar a view:

```python

from rest_framework import serializers
from rest_framework import viewsets

from livros.models import Livro


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        # campos que queremos serializar
        fields = ('id', 'titulo', 'ano')


class LivroView(viewsets.ModelViewSet):
    queryset = Livro.objects.all() # filtra todos os livros
    serializer_class = LivroSerializer # classe de serializer que será usada  
    http_method_names = ['get', 'post', 'put', 'delete']  # métodos http permitidos
```

### Mapeando as urls do app

No app livros será necessário criar um arquivo chamado urls.py com o conteúdo:

```python
from django.urls import path, include
from rest_framework import routers

from livros.views import LivroView


router = routers.DefaultRouter()
router.register('livros', LivroView)  # nome do objeto da view

urlpatterns = [
    path('livros/', include(router.urls)),  # nome do app
]
```

Desta maneira teremos definido o endpoint http://127.0.0.1:8000/livros/livros/ (get, post, put e delete), onde o primeiro "livros" é referente ao nome do app e o segundo é referente ao objeto livro.

Da mesma forma, futuramente podemos ter:
- http://127.0.0.1:8000/livros/autores
- http://127.0.0.1:8000/livros/editoras

Para isso iremos registrar no router as views dos autores e editoras:

```python
...
router = routers.DefaultRouter()
router.register('livros', LivroView)  # nome do objeto da view
# router.register('autores', AutorView)  # nome do objeto da view
# router.register('editoras', EditoraView)  # nome do objeto da view


urlpatterns = [
    path('livros/', include(router.urls)),  # nome do app
]
...
```

No urls.py que já existe no package "livraria" será necessário incluir as urls do app livros:

```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('livros.urls')),  # incluir urls do app livros
]
```

Após estes passos, ao acessar a url http://127.0.0.1:8000/livros/livros/ teremos acesso a uma documentação gerada automaticamente pelo próprio DRF, onde vamos conseguir fazer as opções GET todos e POST:

![drf](figuras/drf.png)

Acessando http://127.0.0.1:8000/livros/1 ou qualquer id existente, vamos ter acesso ao GET, PUT e DELETE:

![drf-id](figuras/drf-id.png)

Isto é possível pois a classe LivroView herda da classe ModelViewSet do DRF e ela implementa os métodos:

- create() - POST
- list - GET todos
- retrieve - GET por id
- update - PUT
- delete - DELETE

Vamos dar uma olhada no retrieve, por exemplo:

```python
class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

Ele recupera o objeto relacionado ao id enviado na url a partir do método get_object() e salva na variável instance. Depois ele recupera a classe de serializer que especificamos na view e utiliza para serializar os dados de instance. Por fim, retorna os dados como um objeto da classe Response(), que retorna um json juntamente com um status code (e erros se houverem). 

Caso precisemos de algum comportamento específico, os métodos padrão podem ser sobreescritos na view.

O serializer já vai fazer algumas validações padrão, como se o tipo do dado enviado condiz com o que está especificado no model ou se estão faltando dados obrigatórios, por exemplo.

Ainda no arquivo models.py do app livro vamos criar o model Autor e também vincular o autor ao livro:

```python
from django.db import models


class Autor(models.Model):
    # o id é gerado automaticamente
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()


class Livro(models.Model):
    # o id é gerado automaticamente
    titulo = models.CharField(max_length=255)
    ano = models.IntegerField()
    autor = models.ForeignKey(
        Autor, 
        related_name='livros_autor', # o related_name é usado para recuperar os livros a partir do autor
        on_delete=models.CASCADE,  # se o autor for excluído o cascade vai fazer o livro ser excluído também
        null=True  # para evitar problema nos livros que foram criados antes da tabela Autor
    )
```

Cadastro do autor no admin.py:

```python
from django.contrib import admin

from livros.models import Livro, Autor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    # campos que vão aparecer na listagem
    list_display = ('id', 'nome', 'data_nascimento')


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # campos que vão aparecer na listagem
    list_display = ('id', 'titulo', 'ano')

```

Vamos rodar o comando para gerar as migrations: `python manage.py makemigrations`. Isso vai gerar o arquivo 0002_autor_livro_autor.py. Podemos renomear este arquivo se preferirmos, mas antes de rodar o migrate. Após rodar o migrate o nome dessa migration fica registrado em uma tabela do Django para contrele de migrations. 

Vamos rodar o comando para aplicar as migrations no banco: `python manage.py migrate`.

Para fazer um pequeno teste, vamos alterar o nome da migration após rodar o migrate: 0002_autor.py. Ao tentar rodar o migrate de novo vai acontecer um erro:

```different
...
django.db.utils.OperationalError: table "livros_autor" already exists
```

Isso acontece pois o Django usa o nome das migrations para saber o que já rodou ou não. Então ele entende 0002_autor.py como se fosse uma migration nova e tenta rodar novamente. O problema é que a tabela Autor já foi criada no banco ao rodar a migration pela primeira vez com o nome original, e aí o erro acontece. Por isso o nome deve ser alterado antes do migrate se for desejado. Para corrigir o erro vamos voltar para o nome original: 0002_autor_livro_autor.py. Agora ao rodar o migrate novamente a mensgem deve ser:

```different
No migrations to apply.
```

Vamos criar o serializer e a view do autor:

```python

from rest_framework import serializers
from rest_framework import viewsets

from livros.models import Livro, Autor


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        # campos que queremos serializar
        fields = ('id', 'nome', 'data_nascimento')


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        # campos que queremos serializar
        fields = ('id', 'titulo', 'ano', 'autor')  # vamos adicionar aqui o autor também


class AutorView(viewsets.ModelViewSet):
    queryset = Autor.objects.all() # filtra todos os autores
    serializer_class = AutorSerializer # classe de serializer que será usada  
    http_method_names = ['get', 'post', 'put', 'delete']  # métodos http permitidos


class LivroView(viewsets.ModelViewSet):
    queryset = Livro.objects.all() # filtra todos os livros
    serializer_class = LivroSerializer # classe de serializer que será usada  
    http_method_names = ['get', 'post', 'put', 'delete']  # métodos http permitidos
```

Vamos adicionar as urls no urls.py do app livros:

```python
from django.urls import path, include
from rest_framework import routers

from livros.views import LivroView, AutorView


router = routers.DefaultRouter()
router.register('livros', LivroView)  # nome do objeto da view
router.register('autores', AutorView)

urlpatterns = [
    path('livros/', include(router.urls)),  # nome do app
]
```

Agora ao abrir a url http://127.0.0.1:8000/livros/autores/ poderemos cadastrar um novo autor.

Ao abrir a url http://127.0.0.1:8000/livros/livros/ e tentar cadastrar um livro novo, terá aparecido um campo de select para escolher o autor:

![livro-autor](figuras/livro-autor.png)

A opção vai aparecer com um nome estranho: "Autor object (1)". Isto pode ser melhorado adicionado um método na classe Autor:

```python
    def __str__(self) -> str:
        return self.nome
```

Agora, ao atualizar a página dos livros a opção deve aparecer mais amigável no select.

Ao fazer o get dos livros, o autor vem apenas com o id:

```json
...
    {
        "id": 2,
        "titulo": "Lugar nenhum",
        "ano": 2000,
        "autor": 1
    }
...
```

Para trazer os dados do autor dentro do livro, vamos quebrar o LivroSerializer em 2:
- Primeiro vamos renomer o LivroSerializer para LivroWriteSerializer:

```python
# será usado para as operações de post, put
class LivroWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        # campos que queremos serializar
        fields = ('id', 'titulo', 'ano', 'autor')  # vamos adicionar aqui o autor também
```

- Depois vamos criar um LivroReadSerializer:

```python
# será usado para o get
class LivroReadSerializer(serializers.ModelSerializer):
    autor = AutorSerializer()

    class Meta:
        model = Livro
        # campos que queremos serializar
        fields = ('id', 'titulo', 'ano', 'autor')  # vamos adicionar aqui o autor também
```

Vamos atualizar a view do livro:

```python
class LivroView(viewsets.ModelViewSet):
    queryset = Livro.objects.all() # filtra todos os livros
    serializer_class = LivroReadSerializer # classe de serializer que será usada  
    http_method_names = ['get', 'post', 'put', 'delete']  # métodos http permitidos

    def get_serializer_class(self):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return LivroWriteSerializer
```

### Alterando o idioma para português

Alterar no settings.py:

```python
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
```

Agora o admin já deve ficar em português:

![admin-pt](figuras/admin-pt.png)
