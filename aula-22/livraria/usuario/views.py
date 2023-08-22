from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS
from django.contrib.auth.models import User


class UsuarioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff']
        read_only_fields = ['last_login', 'data_joined']


class UsuarioReadSerializer(serializers.ModelSerializer):
    # sobre escrevemos os campos groups e user_permissions para poder customizar
    groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff']

    # métodos chamados de get_campo permitem alterar o valor que queremos retornar para o campo
    def get_groups(self, instance):
        # percorremos todos os grupos da instância e montamos uma lista com os nomes para retornar no lugar dos códigos
        group_names = []
        for group in instance.groups.all():
            group_names.append(group.name)
        return group_names
    
    def get_user_permissions(self, instance):
        # percorremos todas as permissões da instância e montamos uma lista com os nomes para retornar no lugar dos códigos
        perms_names = []
        for perm in instance.user_permissions.all():
            perms_names.append(perm.codename)
        return perms_names


class UsuarioView(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class = UsuarioReadSerializer
    # a criação deve ser feita pelo endpoint de registro e não será possível excluir, apenas inativar
    http_method_names = ['get', 'put']  

    # sobre escrevemos o get_serializer_class para poder alternar entre read e write
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return UsuarioWriteSerializer
