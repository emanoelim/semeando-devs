# Permissões a nível de objeto

Até então nós estamos considerando que para acessar uma view, o usuário deve ter as permissões corretas:

- create: add_model;
- update: change_model;
- list/retrieve: view_model;
- delete: delete_model.

Isso está sendo controlado na classe abaixo (aula 20):

```python
from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'OPTIONS': [],
        'HEAD': [],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # verifica se o usuário tem permissão para acessar a view de acordo com o método http solicitado
    # vamos manter o comportamento padrão
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    # este método poderia ser sobreescrito no caso de um objeto livro, por exemplo, pertencer a uma filial x da livraria
    # e apenas usuários da filial x pudessem acessar o livro. Neste caso, livro e user teriam que ter uma fk de "empresa"
    # para fazer esta comparação.
    # vamos manter o padrão
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(self, request, view, obj)
```

Vamos considerar o exemplo apresentado durante a aula 21:
- Tenho uma tabela Atividade que contém a FK do Usuario, para indicar qual usuário criou a atividade:

```python
class Atividade(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
```

- Em um list/retrieve a atividade só deve aparecer para o usuário que criou ela.


## List

Para o list podemos tratar diretamente em cada view onde for necessário, sobreescrevendo o  método get_queryset():

```python
...
class AtividadeView(ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    http_method_names = ['post', 'get', 'put', 'delete']

    def get_queryset(self):
        return Atividade.objects.filter(usuario=self.request.user)
```

Adicionando este método na view, a listagem vai filtrar apenas atividades que foram criadas pelo usuário.


## Retrieve

Para o retrieve podemos fazer este bloqueio através do método has_object_permission(), onde podemos filtrar que um objeto só possa ser acessado caso o usuário que esteja tentando fazer o acesso seja o seu usuário criador:

```python
    def has_object_permission(self, request, view, obj):
        # a partir do objeto, recuperar qual é o model
        model = type(obj)

        # Se o model não tiver FK para Usuario, deduzimos que ele pode ser acessado por todos
        if not hasattr(model, 'usuario'):
            return True

        # Se o usuário da request for o mesmo do objeto, então ele pode acessar
        if request.user == obj.usuario:
            return True

        # Acesso bloqueado em qualquer outro caso
        return False
```

Desta forma, não é necessário tratar em cada view. Todas as views vão passar pela função has_object_permission() quando for um get id, update ou delete, então vai cobrir todo caso. 