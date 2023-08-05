import requests
from rest_framework.authentication import BaseAuthentication

from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class ArbacheAuthentication(BaseAuthentication):
    """
        Autenticação e identificação do level do perfil
        logado no ambiente Arbache.
    """

    def authenticate(self, request):

        session = requests.Session()

        perfil = request.query_params.get('perfil')
        authorization = request.headers.get('Authorization', False)

        if not authorization:
            raise AuthenticationFailed('Falha na autenticação.')
        try:
            response = session.get(
                f'{settings.ARBACHE_AUTHENTICATION_URL}/backend/autorizacao/?perfil={perfil}', # noqa
                headers={
                    'Authorization': request.headers['Authorization'],
                    'content-type': 'application/json'
                }
            )
        except Exception:
            raise AuthenticationFailed('Falha na autenticação.')

        if response.status_code != 200:
            raise AuthenticationFailed('Falha na autenticação.')

        response_obj = response.json()
        request.user = response_obj['email']
        request.level = response_obj['level']
        request.perfil = perfil
        request.token = request.headers['Authorization'].split(' ')[-1]

        return (request.user, True)


class ArbacheAppAuthentication(BaseAuthentication):
    """
        Autenticação de aplicação através de token
        validado pelo CRM Arbache.
    """

    def authenticate(self, request):
        session = requests.Session()

        authorization = request.headers.get('Authorization', False)

        if not authorization:
            raise AuthenticationFailed('Falha na autenticação.')
        try:
            response = session.get(
                f'{settings.ARBACHE_AUTHENTICATION_URL}/backend/app/autorizacao/', # noqa
                headers={
                    'Authorization': request.headers['Authorization'],
                    'content-type': 'application/json'
                },
            )
        except Exception:
            raise AuthenticationFailed('Falha na autenticação.')

        if response.status_code != 200:
            raise AuthenticationFailed('Falha na autenticação.')

        request.token = request.headers['Authorization'].split(' ')[-1]

        return (request.user, True)
