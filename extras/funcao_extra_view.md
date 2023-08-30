### Criando funções extra para a view

Caso precise criar uma função além das padrão do ModelViewSet, você pode usar o decorator @action.

No exemplo, a EmpresaView fica no módulo empresa, logo, será gerado o endpoint: ".../empresas/empresas/analise":

```python
from rest_framework.decorators import action
...

class EmpresaView(ModelViewSet):
    ...

    @action(methods=['get'], detail=False, url_path='analise')
    def get_analises_empresa(self, request, pk, *args, **kwargs):
        """
        Retorna todas as análises que pertencem à uma empresa.
        """
        empresa = request.query_params.get('empresa')
        if not empresa:
            return Response(status=HTTP_400_BAD_REQUEST, data={'empresa': ['Informe a empresa.']})
            
        analises = Analise.objects.filter(empresa=empresa)
        serializer = AnaliseSerializer(analises, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
```
