from django.contrib import admin

from pedidos.models import Pedido, PedidoLivros, Cupom


class PedidoLivrosInline(admin.TabularInline):
    model = PedidoLivros
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data')
    inlines = [PedidoLivrosInline]


@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'percentual_desconto', 'desconto_maximo')
