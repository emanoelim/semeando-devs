# Generated by Django 4.2.2 on 2023-06-24 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0002_autor_livro_autor'),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoLivros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livros.livro')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido')),
            ],
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='livros',
        ),
        migrations.AddField(
            model_name='pedido',
            name='livros',
            field=models.ManyToManyField(through='pedidos.PedidoLivros', to='livros.livro'),
        ),
    ]
