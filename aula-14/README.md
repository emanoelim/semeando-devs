# Aula 14

## Criando um arquivo .env

Algumas variáveis estão diretamente no arquivo de settings.py, como é o caso da SECRET_KEY. Este é um exemplo de variável que não deve ficar fixa no código. O Django utiliza esta variável para fins de criptografia e deixar ela exposta pode fazer com que pessoas mal intencionadas a utilizem para gerar um token de acesso para a API, por exemplo.

Esta e outras variáveis podem ser armazenadas em um arquivo separado, que é acessado pelo settings.py, um arquivo chamado .env:

```different
SECRET_KEY = 'django-insecure-mht^eh=x718t@=pk*__)2cya5zgv^#awzg0_*5*5e4tg97@me_'
```

Quando o projeto estiver rodando localmente, o Django irá pegar as variáveis desse arquivo .env. Quando estiver rodando em um servidor, o servidor poderá ser condigurado para guardar essas variáveis.

Vamos instalar esta biblioteca que vai facilitar para ler as variáveis no settings.py: https://pypi.org/project/python-decouple/

```different
pip install python-decouple
```

No ínicio do settings.py será ncessário fazer o import:

```python
from decouple import config
```

E no lugar da variável fixa, vamos deixar:

```python
SECRET_KEY = config('SECRET_KEY')  # mesmo nome que está no arquivo .env
```

O projeto deve rodar normalmente após esse ajuste.

Além disso é necessário proteger o arquivo .env para que ele não seja enviado para um repositório git. Para isto utilizamos um arquivo chamado .gitignore.

Neste repositório do curso já temos um. Vamos adicionar o nome do arquivo .env nele:

```different
.venv/
__pycache__/
.env
```

Ele já contem algumas outras linhas que indicam que não seja enviada a pasta da .venv e também pastas __ pycache __, que são geradas após a compilação. Os arquivos descritos neste arquivo não serão enviados ao fazer um "git commit" para enviar as alterações do projeto para um repositório.

