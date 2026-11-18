"""Testes da capability `configuration` (specs/configuration/spec.md)."""

import importlib
import logging
import sys

import pytest
from pydantic import SecretStr, ValidationError

from icpc_tutor.config import Settings, get_settings

VARIAVEIS = ("APP_ENV", "LOG_LEVEL", "API_TOKEN")


@pytest.fixture
def ambiente_limpo(monkeypatch, tmp_path):
    """Isola o teste do ambiente real: sem variáveis do tutor e sem `.env`.

    O diretório de trabalho vira uma pasta temporária vazia, então o `.env`
    real do desenvolvedor nunca é lido.
    """
    for nome in VARIAVEIS:
        monkeypatch.delenv(nome, raising=False)
    monkeypatch.chdir(tmp_path)
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_inicializa_com_configuracao_completa_no_ambiente(ambiente_limpo, monkeypatch):
    """configuration: Inicialização com configuração completa"""
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = get_settings()

    assert settings.app_env == "prod"
    assert settings.log_level == "DEBUG"
    assert get_settings() is settings  # validado uma vez e reaproveitado


def test_inicializa_com_configuracao_completa_no_arquivo_env(ambiente_limpo):
    """configuration: Inicialização com configuração completa"""
    (ambiente_limpo / ".env").write_text("APP_ENV=dev\nLOG_LEVEL=WARNING\n")

    settings = get_settings()

    assert settings.app_env == "dev"
    assert settings.log_level == "WARNING"


def test_configuracao_obrigatoria_ausente_interrompe(ambiente_limpo):
    """configuration: Configuração obrigatória ausente

    A fixture de `conftest.py` bloqueia a rede: se alguma conexão fosse aberta
    antes da validação, o erro seria `RedeBloqueadaError`, não `ValidationError`.
    """
    with pytest.raises(ValidationError) as erro:
        get_settings()

    mensagem = str(erro.value)
    assert "app_env" in mensagem
    assert "Field required" in mensagem


def test_valor_com_tipo_invalido_interrompe(ambiente_limpo, monkeypatch):
    """configuration: Valor com tipo inválido"""
    monkeypatch.setenv("APP_ENV", "staging")

    with pytest.raises(ValidationError) as erro:
        get_settings()

    mensagem = str(erro.value)
    assert "app_env" in mensagem
    assert "'dev' or 'prod'" in mensagem  # o tipo esperado


def test_configuracao_opcional_omitida_usa_padrao(ambiente_limpo, monkeypatch):
    """configuration: Configuração opcional omitida"""
    monkeypatch.setenv("APP_ENV", "dev")

    assert get_settings().log_level == "DEBUG"


def test_import_nao_le_configuracao(ambiente_limpo):
    """configuration: Configuração validada na inicialização (não no import)"""
    sys.modules.pop("icpc_tutor.config", None)

    modulo = importlib.import_module("icpc_tutor.config")

    assert hasattr(modulo, "get_settings")


class _SettingsComSegredo(Settings):
    """Modelo de teste: ainda não existe segredo real nesta fatia."""

    api_token: SecretStr


SEGREDO = "tok-super-secreto-123456"


def test_segredo_valido_nao_aparece_em_saidas(ambiente_limpo, monkeypatch, caplog):
    """configuration: Erro envolvendo um segredo (o valor nunca aparece em saídas)"""
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("API_TOKEN", SEGREDO)

    settings = _SettingsComSegredo()
    with caplog.at_level(logging.INFO):
        logging.getLogger("teste").info("config carregada: %s / %r", settings, settings)

    assert settings.api_token.get_secret_value() == SEGREDO
    assert SEGREDO not in repr(settings)
    assert SEGREDO not in str(settings)
    assert SEGREDO not in caplog.text


def test_segredo_ausente_cita_so_o_nome(ambiente_limpo, monkeypatch):
    """configuration: Erro envolvendo um segredo (ausente)"""
    monkeypatch.setenv("APP_ENV", "dev")

    with pytest.raises(ValidationError) as erro:
        _SettingsComSegredo()

    assert "api_token" in str(erro.value)


def test_segredo_invalido_nao_vaza_na_mensagem(ambiente_limpo, monkeypatch, caplog):
    """configuration: Erro envolvendo um segredo (inválido)

    Outro campo inválido faz a validação falhar com o segredo presente: a
    mensagem cita nomes, mas não repete nenhum valor recebido.
    """
    monkeypatch.setenv("APP_ENV", SEGREDO)  # valor inválido que é um segredo
    monkeypatch.setenv("API_TOKEN", SEGREDO)

    with pytest.raises(ValidationError) as erro, caplog.at_level(logging.INFO):
        try:
            _SettingsComSegredo()
        except ValidationError:
            logging.getLogger("teste").exception("falha na configuração")
            raise

    assert "app_env" in str(erro.value)
    assert SEGREDO not in str(erro.value)
    assert SEGREDO not in repr(erro.value)
    assert SEGREDO not in caplog.text
