from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from pedidos.models import Pedido, PedidoLivro, Cupom
from clientes.views import ClienteSerializer
from livros.views import LivroReadSerializer


class PedidoLivroWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoLivro
        fields = ('livro', 'quantidade')


class PedidoLivroReadSerializer(serializers.ModelSerializer):
    livro = LivroReadSerializer()

    class Meta:
        model = PedidoLivro
        fields = ('livro', 'quantidade')


class PedidoWriteSerializer(serializers.ModelSerializer):
    livros = PedidoLivroWriteSerializer(many=True, source='pedidolivro_set')
    cupom = serializers.CharField(max_length=15, required=False)

    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'livros', 'total', 'cupom')

    def validate_cupom(self, value):
        value = value.upper()
        cupom = Cupom.objects.filter(nome=value).first()
        if not cupom:
            raise serializers.ValidationError('Cupom inválido.')
        return cupom

    def create(self, validated_data):
        """
        {
            "cliente": 1,
            "livros": [
                {
                "livro": 1,
                "quantidade": 2
                }
            ]
        }
        """
        livros = validated_data.pop('pedidolivro_set')
        instance = Pedido.objects.create(**validated_data)
        for livro in livros:
            PedidoLivro.objects.create(pedido=instance, livro=livro['livro'], quantidade=livro['quantidade'])
        instance.total = instance.calcular_total()
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        livros = validated_data.pop('pedidolivro_set')
        instance.livros.clear()
        for livro in livros:
            PedidoLivro.objects.create(pedido=instance, livro=livro['livro'], quantidade=livro['quantidade'])
        instance = super().update(instance, validated_data)
        instance.total = instance.calcular_total()
        instance.save()
        return instance


class PedidoReadSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    livros = PedidoLivroReadSerializer(many=True, source='pedidolivro_set')

    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'livros', 'total', 'cupom')


class PedidoView(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoReadSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return PedidoWriteSerializer
