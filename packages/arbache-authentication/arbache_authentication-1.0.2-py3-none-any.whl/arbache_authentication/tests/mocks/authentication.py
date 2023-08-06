from abc import ABC


class ResponseMock(ABC):
    def __init__(self, status_code=None, data=None) -> None:
        self.status_code = status_code
        self.data = data


class ResponseMockSucesso(ResponseMock):
    def __init__(self, status_code=None, data=None) -> None:
        self.data = {
            "email": "williames@arbache.com",
            "level": 3
        }
        super().__init__(status_code=200, data=self.data)

    def json(self):
        return self.data


class ResponseMockAplicacaoSucesso(ResponseMock):
    def __init__(self, status_code=None, data=None) -> None:
        self.data = {}
        super().__init__(status_code=200, data=self.data)


class ResponseMockFalhaPerfil(ResponseMock):
    def __init__(self, status_code=None, data=None) -> None:
        self.data = {
            "detail": "Perfil inválido"
        }
        super().__init__(status_code=403, data=self.data)

    def json(self):
        return self.data


class SessionMock(ABC):
    def __init__(self, status_code=None, data=None) -> None:
        self.response = {}

    def get(self, url, headers):
        return self.response


class SessionMockSucesso(SessionMock):

    def __init__(self, status_code=None, data=None) -> None:
        self.response = ResponseMockSucesso()

    def get(self, url, headers):
        return self.response


class SessionMockFalhaPerfil(SessionMock):

    def __init__(self, status_code=None, data=None) -> None:
        self.response = ResponseMockFalhaPerfil()

    def get(self, url, headers):
        return self.response


class SessionMockAplicacaoSucesso(SessionMock):
    def __init__(self, status_code=None, data=None) -> None:
        self.response = ResponseMockAplicacaoSucesso()
        self.user = None

    def get(self, url, headers):
        return self.response
