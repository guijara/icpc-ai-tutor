"""Configuração do tutor, lida do ambiente e do arquivo `.env`.

Nada é lido no import: a validação acontece na primeira chamada de
`get_settings()`, para que importar o pacote nunca falhe por falta de `.env`.

Convenção para segredos: todo campo secreto usa `SecretStr`. O valor só sai
com `.get_secret_value()`; `repr`, `str` e logs mostram `**********`.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações aceitas pelo tutor. Cada campo aparece no `.env.example`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # Mensagens de erro não repetem o valor recebido (protege segredos).
        hide_input_in_errors=True,
    )

    app_env: Literal["dev", "prod"]
    """Obrigatória e sem padrão, para ninguém subir em produção por esquecimento."""

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    """Opcional; padrão documentado `INFO`."""


@lru_cache
def get_settings() -> Settings:
    """Valida a configuração na primeira chamada e reaproveita o resultado.

    Levanta `pydantic.ValidationError` nomeando cada configuração ausente ou
    inválida, o que interrompe a inicialização antes de qualquer conexão.
    """
    return Settings()
