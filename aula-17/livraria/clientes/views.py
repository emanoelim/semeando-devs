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
        read_only_fields = ('rua', 'cidade', 'uf')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.preencher_endereco()
        return instance
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.preencher_endereco() 
        return instance  


class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all() 
    serializer_class = ClienteSerializer 
    http_method_names = ['get', 'post', 'put', 'delete']  


class EnderecoView(viewsets.ModelViewSet):
    queryset = Endereco.objects.all() 
    serializer_class = EnderecoSerializer 
    http_method_names = ['get', 'post', 'put', 'delete']  
