from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from pedidos.models import Pedido, PedidoLivros
from clientes.views import ClienteSerializer
from livros.views import LivroReadSerializer


class PedidoLivrosWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoLivros
        fields = ('livro', 'quantidade')


class PedidoLivrosReadSerializer(serializers.ModelSerializer):
    livro = LivroReadSerializer()

    class Meta:
        model = PedidoLivros
        fields = ('livro', 'quantidade')


class PedidoWriteSerializer(serializers.ModelSerializer):
    livros = PedidoLivrosWriteSerializer(source='pedidolivros_set', many=True)

    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'livros')
    
    def create(self, validated_data):
        livros = validated_data.pop('pedidolivros_set')
        instance = Pedido.objects.create(**validated_data)
        for livro in livros:
            PedidoLivros.objects.create(pedido=instance, livro=livro.get('livro'), quantidade=livro.get('quantidade'))
        return instance

    def update(self, instance, validated_data):
        livros = validated_data.pop('pedidolivros_set')
        instance.livros.clear()
        for livro in livros:
            PedidoLivros.objects.create(pedido=instance, livro=livro.get('livro'), quantidade=livro.get('quantidade'))
        return instance


class PedidoReadSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    livros = PedidoLivrosReadSerializer(source='pedidolivros_set', many=True)

    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'livros', 'total')


class PedidoView(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoReadSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return PedidoWriteSerializer
