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
