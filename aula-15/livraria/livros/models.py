from django.db import models


class Autor(models.Model):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()

    def __str__(self) -> str:
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    ano = models.IntegerField()
    autor = models.ForeignKey(
        Autor, 
        related_name='livros_autor',  # o related_name é usado para recuperar os livros a partir do autor
        on_delete=models.CASCADE,  # se o autor for excluído o cascade vai fazer o livro ser excluído também
        null=True  # para evitar problema nos livros que foram criados antes da tabela Autor
    )
    valor = models.DecimalField(default=0, max_digits=10, decimal_places=2)  # novo campo, default=0 para os livros que já existem

    def __str__(self) -> str:
        return self.titulo

