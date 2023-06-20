from rest_framework import serializers
from rest_framework import viewsets

from clientes.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nome', 'cpf', 'data_nascimento', 'email')


class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all() 
    serializer_class = ClienteSerializer 
    http_method_names = ['get', 'post', 'put', 'delete']  
