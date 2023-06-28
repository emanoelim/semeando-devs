from django.contrib import admin

from pedidos.models import Pedido, PedidoLivro, Cupom


class PedidoLivroInline(admin.TabularInline):
    model = PedidoLivro
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data')
    inlines = [PedidoLivroInline]


@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
