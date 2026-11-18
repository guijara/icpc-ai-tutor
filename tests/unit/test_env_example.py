"""Contrato do `.env.example` (specs/configuration/spec.md)."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from icpc_tutor.config import Settings

RAIZ = Path(__file__).resolve().parents[2]
EXEMPLO = RAIZ / ".env.example"

# Formatos típicos de chaves e tokens que nunca devem estar no exemplo.
PARECE_SEGREDO = [
    re.compile(r"^sk-"),  # chaves de API no estilo OpenAI/Anthropic
    re.compile(r"^AKIA[0-9A-Z]{16}$"),  # access key da AWS
    re.compile(r"^(ghp|gho|github_pat)_"),  # tokens do GitHub
    re.compile(r"^xox[abp]-"),  # tokens do Slack
    re.compile(r"^eyJ"),  # JWT (ex.: chaves do Supabase)
    re.compile(r"^[A-Za-z0-9_\-.+/=]{24,}$"),  # string longa e aleatória
]


def _linhas_do_exemplo() -> list[str]:
    return EXEMPLO.read_text(encoding="utf-8").splitlines()


def _variaveis_do_exemplo() -> dict[str, str]:
    variaveis = {}
    for linha in _linhas_do_exemplo():
        if linha.strip() and not linha.lstrip().startswith("#"):
            nome, _, valor = linha.partition("=")
            variaveis[nome.strip()] = valor.strip()
    return variaveis


def test_exemplo_lista_todas_as_configuracoes():
    """configuration: Novo desenvolvedor configura o ambiente"""
    esperadas = {nome.upper() for nome in Settings.model_fields}

    assert esperadas <= set(_variaveis_do_exemplo())


def test_cada_variavel_tem_comentario_na_linha_anterior():
    """configuration: Arquivo de exemplo versionado sem valores reais (um comentário por linha)"""
    linhas = _linhas_do_exemplo()
    for i, linha in enumerate(linhas):
        if linha.strip() and not linha.lstrip().startswith("#"):
            assert i > 0 and linhas[i - 1].lstrip().startswith("#"), linha


def test_exemplo_copiado_para_env_inicializa(monkeypatch, tmp_path):
    """configuration: Novo desenvolvedor configura o ambiente"""
    for nome in _variaveis_do_exemplo():
        monkeypatch.delenv(nome, raising=False)
    shutil.copy(EXEMPLO, tmp_path / ".env")
    monkeypatch.chdir(tmp_path)

    Settings()  # não levanta erro


@pytest.mark.parametrize("nome,valor", sorted(_variaveis_do_exemplo().items()))
def test_exemplo_nao_tem_valor_que_pareca_segredo(nome, valor):
    """configuration: Verificação de segredos no repositório"""
    for padrao in PARECE_SEGREDO:
        assert not padrao.search(valor), f"{nome} parece conter um segredo"


def test_env_real_e_ignorado_pelo_git():
    """configuration: Verificação de segredos no repositório"""
    ignorado = subprocess.run(
        ["git", "check-ignore", "-q", ".env"], cwd=RAIZ, check=False
    )
    exemplo = subprocess.run(
        ["git", "check-ignore", "-q", ".env.example"], cwd=RAIZ, check=False
    )

    assert ignorado.returncode == 0, ".env precisa estar no .gitignore"
    assert exemplo.returncode == 1, ".env.example precisa ser versionado"
