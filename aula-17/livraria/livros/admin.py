from django.contrib import admin

from livros.models import Livro, Autor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    # campos que vão aparecer na listagem
    list_display = ('id', 'nome', 'data_nascimento')


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # campos que vão aparecer na listagem
    list_display = ('id', 'titulo', 'ano')
