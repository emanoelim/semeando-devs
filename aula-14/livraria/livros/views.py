
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from livros.models import Livro, Autor


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        # campos que queremos serializar
        fields = ('id', 'nome', 'data_nascimento')


class LivroWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        # campos que queremos serializar
        fields = ('id', 'titulo', 'ano', 'autor')  # vamos adicionar aqui o autor também


class LivroReadSerializer(serializers.ModelSerializer):
    autor = AutorSerializer()

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
    serializer_class = LivroReadSerializer # classe de serializer que será usada  
    http_method_names = ['get', 'post', 'put', 'delete']  # métodos http permitidos

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return LivroWriteSerializer
