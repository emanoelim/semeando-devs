from django.urls import path, include
from rest_framework import routers

from clientes.views import ClienteView, EnderecoView


router = routers.DefaultRouter()
router.register('clientes', ClienteView)
router.register('enderecos', EnderecoView)

urlpatterns = [
    path('clientes/', include(router.urls)),
]
