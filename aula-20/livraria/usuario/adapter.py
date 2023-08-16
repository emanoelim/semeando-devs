from allauth.account.adapter import DefaultAccountAdapter

from livraria.settings import URL_FRONTEND


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f'{URL_FRONTEND}/confirm-email/{emailconfirmation.key}'