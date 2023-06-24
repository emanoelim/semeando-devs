from django.contrib import admin

from pedidos.models import Pedido, PedidoLivros


class PedidoLivrosInline(admin.TabularInline):
    model = PedidoLivros
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data')
    inlines = [PedidoLivrosInline]

