from django.db import models


class Livro(models.Model):
    # o id é gerado automaticamente
    titulo = models.CharField(max_length=255)
    ano = models.IntegerField()
