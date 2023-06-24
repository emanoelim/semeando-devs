from django.urls import path, include
from rest_framework import routers

from pedidos.views import PedidoView


router = routers.DefaultRouter()
router.register('pedidos', PedidoView)

urlpatterns = [
    path('pedidos/', include(router.urls))
]
