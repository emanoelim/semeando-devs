# Customizar link de verificação de email

Por padrão, a lib que usamos vai montar um e-mail de verificação de e-mail com a url da api:

```different
Olá do site 127.0.0.1:8000!

Você está recebendo essa mensagem porque o usuário manu utilizou este e-mail para se cadastrar no site 127.0.0.1:8000.

Para confirmar que isso está correto, clique em http://127.0.0.1:8000/accounts/registration/account-confirm-email/Nw:1qWPWj:Du8Zc0c_KkSR6pllQZG1JmloxPDywyAcIGE4FmofT2j/

Obrigado por usar o site 127.0.0.1:8000!
127.0.0.1:8000
```

Podemos alterar a url que é enviada neste e-mail para que ela direcione para uma página do nosso fronted. Para isso vamos criar um arquivo adapter.py no app usuario. O código basicamente sobreescreve o método get_email_confirmation_url() para que possamos informar uma url customizada no e-mail de confirmação.

```python
from allauth.account.adapter import DefaultAccountAdapter

from livraria.settings import URL_FRONTEND


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f'{URL_FRONTEND}/confirm-email/{emailconfirmation.key}'
```

É possível ver que o código usa uma variável URL_FRONTEND, vamos criar ela no settings, junto com outra variável que "avisa" o Django que agora ele deve usar a nossa classe de adapter em vez da classe padrão:

```python
ACCOUNT_ADAPTER = 'usuario.adapter.CustomAccountAdapter'
URL_FRONTEND = config('URL_FRONTEND', default='http://localhost:4200')
```

Ao salvar e executar novamente a aplicação, o e-mail ficar da seguinte forma:

```different
Olá do site 127.0.0.1:8000!

Você está recebendo essa mensagem porque o usuário manu utilizou este e-mail para se cadastrar no site 127.0.0.1:8000.

Para confirmar que isso está correto, clique em http://localhost:4200/confirm-email/OA:1qOPbH:fi1YaOzTy_9Z6L2z4I_5pg88N3Fa9xqOncFTxRZ1kjF

Obrigado por usar o site 127.0.0.1:8000!
127.0.0.1:8000
```

Agora você pode criar uma página http://localhost:4200/confirm-email/ no seu frontend. Ela pode ser muito simples. Ela não precisa de nenhum form porque vamos extrair a key que chega na url, o usuário não precisará informar nada. No html será necessário exibir apenas uma mensagem de sucesso ou erro após a confirmação do e-mail.

No exemplo abaixo, considere que existe um componente chamado "confirm-email.component", que é chamado na url http://localhost:4200/confirm-email/. O código abaixo é o "confirm-email.component.ts":

```typescript
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from 'app/core/auth/auth.service';
import { Utils } from 'app/utils/utils';

@Component({
  selector: 'app-confirm-email',
  templateUrl: './confirm-email.component.html',
  styleUrls: ['./confirm-email.component.scss']
})
export class ConfirmEmailComponent implements OnInit {

  emailConfimed = false;
  message = '';
  constructor(
    private _authService: AuthService,  // Service que acessa as urls /accounts do backend
    private _activatedRoute: ActivatedRoute  // Service que vai permitir recueprar a key que chega na url de validação de email
    ) {
  }

  ngOnInit(): void {
    // Recupear a key que chega na url
    const key = this._activatedRoute.snapshot.params['key'];

    // A função confirmEmail() faz um POST para a url do backend /accounts/registration/verify-email/, enviando a key
    this._authService.confirmEmail(key)
      .subscribe({
        next: (value) => {
          // Em caso de sucesso, o e-mail já está confirmado e esta variável pode ser usada no html para mostrar uma mensagem de sucesso e algum link para redirecioanar para o login
          this.emailConfimed = true;
        },
        error: (error) => {
          // Em caso de erro, esta variável pode ser usada no html para mostrar uma mensagem de erro
          this.emailConfimed = false;
        }
      })
  }
}
```

Para ver o funcionamento do backend, rodar o app da aula-20, que foi atualizado com as alterações descritas acima.