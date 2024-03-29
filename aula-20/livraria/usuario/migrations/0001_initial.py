# Generated by Django 4.2.2 on 2023-07-31 23:02

import sys

from django.db import migrations


def criar_grupos(apps, schema_editor):
    if 'test' in sys.argv:
        return

    Group = apps.get_model('auth', 'group')
    Permission = apps.get_model('auth', 'permission')

    administrador = Group.objects.create(name='Administrador')
    perms_administrador = Permission.objects.filter(
        codename__in=[
            'add_cliente', 'change_cliente', 'view_cliente', 'delete_cliente',
            'add_endereco', 'change_endereco', 'view_endereco', 'delete_endereco',
            'add_livro', 'change_livro', 'view_livro', 'delete_livro',
            'add_autor', 'change_autor', 'view_autor', 'delete_autor',
            'add_cupom', 'change_cupom', 'view_cupom', 'delete_cupom',
        ]
    )
    administrador.permissions.add(*perms_administrador)

    vendedor = Group.objects.create(name='Vendedor')
    perms_vendedor = Permission.objects.filter(
        codename__in=[
            'add_cliente', 'change_cliente', 'view_cliente', 'delete_cliente',
            'add_endereco', 'change_endereco', 'view_endereco', 'delete_endereco',
            'add_pedido', 'change_pedido', 'view_pedido', 'delete_pedido',
        ]    
    )
    vendedor.permissions.add(*perms_vendedor)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(criar_grupos)
    ]
