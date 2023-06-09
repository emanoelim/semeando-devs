## Instalando o Git
O Git é uma ferramenta pra versionamento de código amplamente utilizado atualmente. Além de manter os códigos em um repoistório online, evitando que você perca o código, ele mantém todo o histórico de alterações e de quem realizou essas alterações. Ele possui estratégias para permitir que vários desenvolvedores trabalhem em um mesmo projeto ou até no mesmo arquivo.

O Github é uma plataforma de gerenciamento de códigos que utiliza o Git como sistema de versionamento. No Github você pode criar repositórios para hospedar os códigos, criar repositórios privados, editar os códigos através da interface, executar "actions" para garantir a qualidade do código, entre outras funcionalidades.

Para instalar:
- Linux: `sudo apt install git-all`
- Windows: instalador no link https://git-scm.com/download/win
- Outros sistemas: https://git-scm.com/downloads

Para configurar usuário e e-mail, abrir o Git Bash (windows) ou um terminal normal no linux e executar os comandos:
- git config --global user.name "FIRST_NAME LAST_NAME"
- git config --global user.email "MY_NAME@example.com"

## Configurando a chave SSH

Acessar sua conta do github no menu "Settings":

![1](imagens/1.png)

Abrir o sub menu "SSH and GPG keys":

![2](imagens/2.png)

Irá aparecer um botão para cadastrar uma nova chave SSH:

![3](imagens/3.png)

Essa chave precisa ser gerada no seu computador. Para isso, abrir o Git Bash (windows) ou um terminal normal no linux e rodar o comando: `ssh-keygen -t ed25519 -C "your_email@example.com"`

Deve mostrar um log como no exemplo abaixo:

```different
Generating public/private ed25519 key pair.
Enter file in which to save the key (/c/Users/emano/.ssh/id_ed25519):
```

Pressionar a tecla Enter. Deve aparecer outra mensagem:

```different
Created directory '/c/Users/emano/.ssh'.
Enter passphrase (empty for no passphrase):
```

Não é necessário preencher, basta pressionar Enter novamente. A seguinte mensagem irá aparecer acompanhada da sua chave SSH:

```different
The key fingerprint is:
CHAVE AQUI
```

A chave ficará no caminho indicado no console, no exemplo, em /c/Users/emano/.ssh/id_ed25519. Existirão dois
aquivos, abrir aquele com a extensão .pub. Copiar seu conteúdo após ssh-ed25519 e colar no input, preenchendo também o campo "Title" e então clicando em "Add SSH key:

![4](imagens/4.png)

Em caso de sucesso, uma nova chave com o título que você criou deve ficar listada em SSH Keys.

Feito isso, você não precisará digitar a senha toda vez que for manipular um repositório.

## Clonando um repositório

Na pasta onde deseja guardar o repositório, abrir o Git Bash (windows) ou um terminal normal no linux. Executar o comando: `git clone git@github.com:emanoelim/semeando-devs.git`.

Na primeira vez em que estiver clonando um projeto, deve aparecer a mensagem abaixo. Você deve digitar "yes" e clicar em Enter.

```different
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Depois disso o repositório será clonado em seu computador.
