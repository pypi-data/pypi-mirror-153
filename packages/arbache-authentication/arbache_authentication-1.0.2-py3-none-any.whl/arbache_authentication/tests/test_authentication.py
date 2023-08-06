import unittest
from uuid import uuid4
from unittest import TestCase
from django.test.utils import override_settings
from django.conf import settings
from unittest.mock import patch
from django.http.request import HttpRequest
from django.core.validators import validate_email
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from arbache_authentication.authentication import (
    ArbacheAuthentication, ArbacheAppAuthentication
)
from arbache_authentication.tests.mocks.authentication import (
    SessionMockSucesso, SessionMockFalhaPerfil,
    SessionMockAplicacaoSucesso
)


class TestAutenticacao(TestCase):

    settings.configure()

    @override_settings(ARBACHE_AUTHENTICATION_URL='http://localhost')
    @patch(
        'requests.Session',
        SessionMockSucesso
    )
    def test_autenticacao_perfil(self):
        """
            Teste:
                Autenticar um usuário e identificar o seu perfil e level de
                acesso
            Regra:
                Para ser autenticado é necessário ter o perfil no query
                parameters e o token de autenticação no headers da request
            Resultado Esperado:
                A requisição terá a adição dos atributos perfil e level,
                além do e-mail do usuário.
        """
        url = f'/backend/jogos/?perfil={uuid4()}'
        request_obj = HttpRequest()
        request_obj.path = url,
        request_obj.content_type = 'application/json'
        request_obj.GET = {'perfil': f'{uuid4()}'}

        request = Request(request_obj)
        request.headers = {
            'Authorization': 'Bearer L0zBeeEC5KxYEHj3Q23dTyRO5xUvCT'
        }

        autenticacao = ArbacheAuthentication().authenticate(request)

        validate_email(request.user)
        assert autenticacao[0] == request.user
        assert hasattr(request, 'level')
        assert hasattr(request, 'perfil')

    @override_settings(ARBACHE_AUTHENTICATION_URL='http://localhost')
    def test_autenticacao_perfil_sem_token(self):
        """
            Teste:
                Tentar autenticar requisição sem passar o token no headers.
            Regra:
                Para ser autenticado é necessário ter o perfil no
                query_parameters e o token de autenticação no headers da
                request.
                Não é possível autenticar um usuário sem o token
            Resultado Esperado:
                Uma exceção AuthenticationFailed é lançada porque não veio
                o token para validar na requisição.
        """

        url = f'/backend/jogos/?perfil={uuid4()}'
        request_obj = HttpRequest()
        request_obj.path = url,
        request_obj.content_type = 'application/json'
        request_obj.GET = {'perfil': f'{uuid4()}'}

        request = Request(request_obj)

        with self.assertRaises(AuthenticationFailed):
            ArbacheAuthentication().authenticate(request)

    @override_settings(ARBACHE_AUTHENTICATION_URL='http://localhost')
    @patch(
        'requests.Session',
        SessionMockFalhaPerfil
    )
    def test_autenticacao_perfil_sem_perfil(self):
        """
            Teste:
                Tentar autenticar uma requisição que não tem o
                perfil informado no query parameters.
            Regra:
                Para ser autenticado é necessário ter o perfil no
                query_parameters e o token de autenticação no
                headers da request
                Não é possível autenticar um usuário sem ter o perfil
                informado na URL
            Resultado Esperado:
                Uma exceção AuthenticationFailed é lançada porque não veio
                o perfil para identificar na requisição.
        """

        url = '/backend/jogos/'
        request_obj = HttpRequest()
        request_obj.path = url,
        request_obj.content_type = 'application/json'

        request = Request(request_obj)
        request.headers = {
            'Authorization': 'Bearer L0zBeeEC5KxYEHj3Q23dTyRO5xUvCT'
        }

        with self.assertRaises(AuthenticationFailed):
            ArbacheAuthentication().authenticate(request)

    @override_settings(ARBACHE_AUTHENTICATION_URL='http://localhost')
    @patch(
        'requests.Session',
        SessionMockAplicacaoSucesso
    )
    def test_autenticacao_aplicacao(self):
        """
            Teste:
                Autenticar uma requisição de uma aplicação através do token
                de acesso localizado no headers da requisição.
            Regra:
                Para uma aplicação ser autenticada, um token de
                autenticação deve estar do headers da request
            Resultado Esperado:
                A request recebe um AnonymousUser()
        """

        url = '/backend/app/autorizacao/'
        request_obj = HttpRequest()
        request_obj.path = url,
        request_obj.content_type = 'application/json'

        request = Request(request_obj)
        request.headers = {
            'Authorization': 'Bearer L0zBeeEC5KxYEHj3Q23dTyRO5xUvCT'
        }
        request.user = True

        autenticacao = ArbacheAppAuthentication().authenticate(request)
        self.assertTrue(autenticacao)

    @override_settings(ARBACHE_AUTHENTICATION_URL='http://localhost')
    def test_autenticacao_aplicacao_sem_token(self):
        """
            Teste:
                Autenticar uma aplicação sem token
            Regra:
                Não é possível autenticar uma aplicação sem informar o token
            Resultado Esperado:
                É lançada exceção AuthenticationFailed
        """

        url = '/backend/app/autorizacao/'
        request_obj = HttpRequest()
        request_obj.path = url,
        request_obj.content_type = 'application/json'

        request = Request(request_obj)

        with self.assertRaises(AuthenticationFailed):
            ArbacheAppAuthentication().authenticate(request)


if __name__ == '__main__':
    unittest.main()
