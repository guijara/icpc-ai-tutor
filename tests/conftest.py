"""Configuração comum dos testes."""

import socket

import pytest


class RedeBloqueadaError(RuntimeError):
    """Um teste padrão tentou acessar a rede."""


@pytest.fixture(autouse=True)
def _bloqueia_rede(request, monkeypatch):
    """Impede que testes padrão abram conexões de rede.

    Bloqueia resolução de nomes e abertura de conexão, então o teste falha
    antes de enviar qualquer byte. Só os testes marcados `llm` ficam liberados,
    porque precisam falar com o modelo.
    """
    if request.node.get_closest_marker("llm"):
        return

    def _negado(*args, **kwargs):
        raise RedeBloqueadaError(
            "Teste padrão tentou acessar a rede. Use um dublê ou marque com @pytest.mark.llm."
        )

    monkeypatch.setattr(socket.socket, "connect", _negado)
    monkeypatch.setattr(socket.socket, "connect_ex", _negado)
    monkeypatch.setattr(socket, "create_connection", _negado)
    monkeypatch.setattr(socket, "getaddrinfo", _negado)
