# Aula 18

## Autenticação

Atualmente a API não tem nenhum tipo de autenticação.

Também não temos usuários, exceto o admin do Django.

A partir de agora vamos permitir que apenas pessoas cadastradas no sistema e com as credenciais corretas consigam utilizar a API.

A estretégia de autenticação que vamos usar é o JWT (JSON Web Token). Ele é um token que vamos enviar junto com cada chamada. 

Até então só tinhamos enviado dados no "body" da request (o json com dados que o backend precisava para fazer um cadastro, por exemplo).

O token será enviado no "header" ou "cabeçalho" da request. O header permite que o cliente e o servidor troquem informações adicionais em uma solicitação http. São informações que não estão relacionadas ao objeto (por exmeplo, o livro, o autor, o pedido).

Existem diferentes tipos de header, sendo um deles o "Authorization" header. Sua sintaxe é:

```different
Authorization: <auth-scheme> <authorization-parameters>
```

Exemplo:

```different
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjo
```

- O cliente (front) envia o username + senha para um endpoint específico do servidor.

- Se os dados estiverem corretos, o servidor gera um token e devolve para o cliente.

- A partir disso, o cliente enviará esse token no header de cada request que fizer. 

- Esse token tem uma validade (usualmente 5 minutos). Após essa validade será necessário obter outro.

- Ao receber a request com esse token, o servidor ira decodificar o token, verificar se ele não está vencido e irá obter as informações do usuário (como permissões que ele tem), devolvendo a resposta solicitada caso esteja tudo certo.

## Vantagens:

- O token é independente. Toda informação que o servidor precisa saber sobre o usuário estão no token, então não é preciso consultar o usuário no banco em toda chamada.

- O token é uma informação que tem uma "assinatura digital". Ele é composto por 3 partes:

![token](https://images.ctfassets.net/cdy7uua7fh8z/7FI79jeM55zrNGd6QFdxnc/80a18597f06faf96da649f86560cbeab/encoded-jwt3.png)

(https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-structure)

A primeira parte é o "header", contém informações sobre o tipo do token e o algoritmo usado para criptografar o conteúdo. Exemplo de header:

```python
{
  "typ": "JWT",
  "alg": "HS256"
}
```

A segunda parte é o "payload", que contém as informações do usuário. Exemplo de payload:

```python
{
  "token_type": "access",
  "exp": 1543828431,
  "jti": "7f5997b7150d46579dc2b49167097e7b",
  "user_id": 1
}
```

A terceira parte é a "assinatura". Ela é gerada usando o header + payload + SECRET_KEY. É por isso que a SECRET_KEY do Django deve ficar protegida. Apenas quem possui esta chave consegue criar um token válido para fornecer ao cliente ou decodificar e validar um token que chega.

## Simplejwt

É uma biblioteca recomentada pelos desenvolvedores do DRF. Ele fornece uma estratégia de autenticação por JWT para o DRF: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/. 

```different
pip install djangorestframework_simplejwt
```

No settings vamos adicionar:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

Também será necessário adicionar no INSTALLED_APPS:

```python
...
'rest_framework_simplejwt'
...
```

Nas urls vamos adicionar duas novas urls:

```python
...
path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
...
```

Os dois novos endpoints já vão aparecer no swagger:

![swagger](figuras/swagger.png)

No endpoint /token, ao enviar usuário e senha, vamos receber um token. Pode ser com as credenciais do admin. O resultado será do tipo:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

"access" será o seu token de acesso. "refresh" é o "refresh token". Quando o token perder a validade, o endpoint /token/refresh/ pode ser usado para obter um token novo, sem precisar fazer o login novamente. Basta enviar o um payload contendo o seu refresh token:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

A resposta será um novo token:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

O refresh token também tem validade, assim como o token, mas o seu tempo de validade é maior. 

## Protegendo as views

Escolha uma view qualquer, exemplo a do cliente e adicione:

```python
class ClienteView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)  # NOVA LINHA
    queryset = Cliente.objects.all() 
    serializer_class = ClienteSerializer 
    http_method_names = ['get', 'post', 'put', 'delete']
```

Ao tentar recuperar os clientes, você terá um erro, pois agora você deve enviar o token no header:

```json
{
  "detail": "As credenciais de autenticação não foram fornecidas."
}
```

Vamos ajustar o swagger para poder adicionar um header com nosso token antes das chamadas:

```python
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'DRF Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
```

Agora, no botão "Authorize", logo ao lado de "Django login", será possível adicionar o header necessário. 

![adicionar_header](figuras/adicionar_header.png)

No input, adicionar "Bearer seu_access_token" e clicar em "Authorize".

Feito isso, deve ser possível acessar as informações do endpoint do cliente.

Seria muito trabalhoso ter que adicionar as permission_classes em toda view, além de que podemos criar uma view nova e esquecer de adicionar, deixando os endpoints abertos.

Vamos adicionar um default no settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [  # AQUI
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

Podemos remover as permission_classes da view. Com esta configuração, todas as views devem ficar protegidas automaticamente.

## Criação de usuários

Vamos criar uma view para cadastro de usuários.

O Django já cria por padrão uma tabela de usuários, que é onde fica cadastrado o admin, por exemplo. Ele utiliza o model User.

Ele possui campos como: username, first_name, last_name, email, is_staff, is_active e date_joined.

Na pasta utils, vamos criar um arquivo views.py, onde vamos criar um serializer para este usuário.

```python
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password_1', 'password_2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
```