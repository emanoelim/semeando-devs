from django.urls import path, include
from rest_framework import routers

from clientes.views import ClienteView


router = routers.DefaultRouter()
router.register('clientes', ClienteView)

urlpatterns = [
    path('clientes/', include(router.urls)),
]
