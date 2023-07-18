# Aula 18

## Autenticação

Atualmente a API não tem nenhum tipo de autenticação.

Também não temos usuários, exceto o admin do Django.

A partir de agora vamos permitir que apenas pessoas cadastradas no sistema e com as credenciais corretas consigam utilizar a API.

A estretégia de autenticação que vamos usar é o JWT (JSON Web Token). Ele é um token que vamos enviar junto com cada chamada. 

Até então só tinhamos enviado dados no "body" da request (o json com dados que o backend precisava para fazer um cadastro, por exemplo).

O token será enviado no "header" ou "cabeçalho" da request. O header permite que o cliente e o servidor troquem informações adicionais em uma solicitação http. São informações que não estão relacionadas ao objeto (por exemplo, o livro, o autor, o pedido).

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

Referência: https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-structure

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

Referência: https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html

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

Primeiramente estamos colocando uma validação no e-mail, para não permitir cadastrar usuários com e-mails iguais.

Normalmente quando o usuário vai se cadastrar no sistema, pedimos a senha 2 vezes, para garantir que ele digitou a senha certa. É por isso que adicionamos também no serializer o password_1 e o password_2. São campos que não estão na model, vamos usar apenas para o input dos dados, então vamos definir eles como write_only. Também queremos que a senha seja forte, então adicionamos na primeira delas adicionamos um validator do DRF. Ele vem desse import:

```python
from django.contrib.auth.password_validation import validate_password
```

Ele irá fazer várias validações como: tamanho da senha, senha muito comum, senha deve conter letras, etc.

Por fim, na class Meta estamos adicionando extra_kwargs para dizer que queremos que o first_name e o last_name sejam obrigatórios, pois por padrão não são (você não precisou adicionar eles pra criar o usuário admin). 

Agora vamos adicionar uma validação para garantir que as duas senhas digitadas são a mesma:

```python
    def validate(self, attrs):
        if attrs['password_1'] != attrs['password_2']:
            raise serializers.ValidationError('As senhas precisam ser iguais.')
        return attrs
```

E por fim vamos sobreescrever o create:

```python

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password_1'])
        user.save()
        return user
```

Primeiro criamos o usuário com username, email, first e last name. Depois adicionamos a senha através do método set_password, que já salva essa senha criptografada.

Agora vamos criar a view:

```python
class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
```

Para esta view não queremos obrigar a informar um token, pois o usuário ainda não existe. Então, vamos deixar permission_classes como "AllowAny", que deixa a view aberta.

Por fim, a view precisa ser adicionada na url:

```python
...
path('sign-up/', SignUpView.as_view(), name='sign_up'),
...
```

O endpoint será listado no swagger e por ele será possível adicionar um usuário novo. Ao abrir o cadastro dele pelo Django admin, no campo senha, você verá:

```different
algoritmo: pbkdf2_sha256 iterações: 600000 salt: 51DxCx**************** hash: R3m0r9**************************************

Senhas brutas não são armazenadas, então não há como visualizar a senha desse usuário, porém você pode mudar a senha usando esse form.
```

Agora já deve ser possível obter um token com este novo usuário.

## Melhorias

O cadastro de usuário que fizemos é bastante simples, não fizemos nada para validação de e-mail, recuperação e troca de senha. Na próxima aula veremos como fazer isto e também o cadastro de novos usuários de maneira mais automatizada com uma biblioteca.