# Tabela de usuários customizada

Caso você precise de um usuário que tenha campos a mais do que o usuário padrão do Django, você não precisa criar uma tabela nova do zero, você pode extender as funcionalidades da tabela User do Django. 

Para fazer isso, podemos criar uma tabela que herda da classe AbstractUser do Django. Exemplo:

```python
class Usuario(AbstractUser):
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.DO_NOTHING)
```

No exemplo, além de ter todos os atributos do usuário padrão do Django, esse usuário vai ter um FK de Empresa, que vai indicar, por exemplo, em qual filial da livraria ele trabalha.

Depois de criar essa tabela, precisamos informar para o Django que agora ele não deve mais usar a tabela padrão (django.contrib.auth.models.User), mas sim a nossa tabela customizada. Isso é feito adicionando esta variável no arquivo settings:

```python
# Auth user model
AUTH_USER_MODEL = 'usuario.Usuario'
```

No meu caso, tenho um app chamado usuario, com um arquivo models.py contendo o model Usuario. Veja que não é necessário passar "usuario.models.Usuario", apenas o "nome_app.Model". 
Para que funcione corretamente o arquivo model.py tem que estar na raíz do app (como já é o padrão do Django mesmo).

Você também vai precisar registrar o novo model no admin.py do app:

```python
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'empresa')
```

Obs.: você provavelmente vai precisar resetar o seu banco de dados para que esta modificação funcione corretamente, pois o Django já precisa criar as migrations certinhas desde o começo do projeto.

Depois disso já é possível trocar nas views e serializers para pegar o model customizado.
