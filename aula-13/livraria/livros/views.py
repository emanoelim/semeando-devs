
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
    