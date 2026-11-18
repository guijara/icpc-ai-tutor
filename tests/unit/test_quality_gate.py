"""Isolamento dos testes (specs/quality-gate/spec.md)."""

import socket
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
ESTE_ARQUIVO = Path(__file__).relative_to(RAIZ).as_posix()
TESTE_LLM = f"{ESTE_ARQUIVO}::test_exemplo_llm_tem_rede_liberada"
TESTE_PADRAO = f"{ESTE_ARQUIVO}::test_chamada_indevida_a_servico_externo_falha"


def _pytest(*args: str) -> subprocess.CompletedProcess[str]:
    """Roda o pytest do projeto num processo separado, com a config do pyproject."""
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", *args],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.llm
def test_exemplo_llm_tem_rede_liberada():
    """Exemplo de teste `llm`: não chama modelo, só confirma que a rede não está bloqueada."""
    assert socket.socket.connect is socket.SocketType.connect
    assert socket.create_connection.__module__ == "socket"


def test_execucao_padrao_nao_roda_testes_llm():
    """quality-gate: Execução padrão da suíte"""
    coletados = _pytest("--collect-only", "-q").stdout

    assert TESTE_LLM not in coletados
    assert TESTE_PADRAO in coletados


def test_execucao_explicita_roda_so_testes_llm():
    """quality-gate: Execução explícita dos testes com LLM"""
    resultado = _pytest("-m", "llm", "-v")

    assert resultado.returncode == 0, resultado.stdout
    assert f"{TESTE_LLM} PASSED" in resultado.stdout
    assert TESTE_PADRAO not in resultado.stdout
    assert "test_config.py" not in resultado.stdout


@pytest.mark.parametrize(
    "tentativa",
    [
        lambda: socket.create_connection(("example.com", 443), timeout=1),
        lambda: socket.socket().connect(("127.0.0.1", 9)),
        lambda: socket.getaddrinfo("example.com", 443),
        lambda: urllib.request.urlopen("https://example.com", timeout=1),
    ],
    ids=["create_connection", "socket.connect", "dns", "urlopen"],
)
def test_chamada_indevida_a_servico_externo_falha(tentativa):
    """quality-gate: Chamada indevida a serviço externo"""
    with pytest.raises(RuntimeError, match="acessar a rede"):
        tentativa()
