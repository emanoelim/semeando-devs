### Recuperar todas as permissões do usuário

O código abaixo adiciona um campo a mais no serializer, chamado "permissions". No método "get_permissions()"
chamamos o método "get_all_permissions()" que faz o conjunto das permissões do usuário + permissões dos grupos do usuário,
então temos a lista completa de permissões.

```python
class UsuarioSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = (
            'id',
            'first_name',
            'last_name',
            ...
            'permissions',
        )

    def get_permissions(self, instance):
        permissions = instance.get_all_permissions()
        return [p.split('.')[1] for p in permissions]
```
