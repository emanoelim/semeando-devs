from django.urls import path, include
from rest_framework import routers

from livros.views import LivroView, AutorView


router = routers.DefaultRouter()
router.register('livros', LivroView)  # nome do objeto da view
router.register('autores', AutorView)

urlpatterns = [
    path('livros/', include(router.urls)),  # nome do app
]