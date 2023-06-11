from django.urls import path, include
from rest_framework import routers

from livros.views import LivroView


router = routers.DefaultRouter()
router.register('livros', LivroView)  # nome do objeto da view

urlpatterns = [
    path('livros/', include(router.urls)),  # nome do app
]