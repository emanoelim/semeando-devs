from django.contrib import admin

from livros.models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # campos que vão aparecer na listagem
    list_display = ('id', 'titulo', 'ano')
