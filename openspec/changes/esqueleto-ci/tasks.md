# Tasks

Convenção: todo teste cita no docstring o cenário da spec que valida (ex.: `"""configuration: Configuração obrigatória ausente"""`). Tarefas `[HUMAN]` são do usuário; o agente para nelas e espera confirmação (ver `CLAUDE.md`).

## 1. Base do projeto

- [x] 1.0 [HUMAN] Instalar o `uv` no notebook; verificar com `uv --version`
- [x] 1.1 [AGENT] Criar `pyproject.toml` com `requires-python = "==3.11.*"`, `.python-version` com `3.11` e o pacote `src/icpc_tutor/__init__.py`; verificar com `uv run python -c "import icpc_tutor, sys; print(sys.version)"` mostrando 3.11 (blocked by: 1.0)
- [x] 1.2 [AGENT] Adicionar `pydantic-settings` como dependência e `ruff` e `pytest` como dependências de desenvolvimento, gerar e versionar o `uv.lock`; verificar que `uv sync --locked` termina sem erro numa pasta limpa

## 2. Configuração

- [x] 2.1 [AGENT] Implementar `Settings` e `get_settings()` em `src/icpc_tutor/config.py` com `APP_ENV` (obrigatória, `dev`/`prod`) e `LOG_LEVEL` (opcional, padrão `INFO`); verificar com testes dos cenários "Inicialização com configuração completa", "Configuração obrigatória ausente", "Valor com tipo inválido" e "Configuração opcional omitida"
- [x] 2.2 [AGENT] Garantir que nenhuma configuração é lida no import do pacote; verificar com um teste que importa `icpc_tutor.config` sem `APP_ENV` definido e não levanta erro
- [x] 2.3 [AGENT] Adotar `SecretStr` para segredos e testar com um modelo de teste o cenário "Erro envolvendo um segredo" (o valor não aparece em `repr`, `str` nem na mensagem de erro)
- [x] 2.4 [AGENT] Criar `.env.example` com `APP_ENV` e `LOG_LEVEL`, um comentário por linha e nenhum valor real; verificar com testes dos cenários "Novo desenvolvedor configura o ambiente" (todo campo de `Settings` aparece no exemplo) e "Verificação de segredos no repositório" (valores vazios ou de exemplo, e `git check-ignore .env` confirma que o `.env` é ignorado)

## 3. Isolamento dos testes

- [x] 3.1 [AGENT] Registrar o marcador `llm` e excluí-lo por padrão na configuração do `pytest`; verificar com testes dos cenários "Execução padrão da suíte" e "Execução explícita dos testes com LLM" (um teste `llm` de exemplo, que não chama modelo, só roda com `-m llm`)
- [x] 3.2 [AGENT] Criar a fixture `autouse` em `tests/conftest.py` que bloqueia conexões de socket, liberada só para testes `llm`; verificar com teste do cenário "Chamada indevida a serviço externo"
- [x] 3.3 [AGENT] Verificar o cenário "Execução sem segredos" rodando `env -i PATH="$PATH" HOME="$HOME" uv run pytest` sem `.env` e confirmando que tudo passa
- [x] 3.4 [AGENT] Adicionar em `docs/conceitos.md` um item `[ENTENDER]` sobre testes em camadas e o marcador `llm`, com pergunta de verificação; verificar que o arquivo segue o formato dos demais itens

## 4. CI

- [x] 4.1 [AGENT] Criar `.github/workflows/ci.yml` com gatilhos `pull_request` e `push` em `develop`, rodando `uv sync --locked`, `ruff check`, `ruff format --check` e `pytest`, sem nenhum segredo; verificar localmente que os mesmos comandos passam
- [x] 4.2 [HUMAN] Autorizar o push na `develop` e confirmar o cenário "Push na develop": o workflow aparece verde na aba Actions
- [x] 4.3 [HUMAN] Validar os cenários "PR aberto com mudanças válidas" e "PR com falha de teste": abrir pelo site um PR de teste com um teste quebrado, confirmar o check vermelho e o nome do teste no relatório, e fechar o PR sem merge
- [x] 4.4 [AGENT] Atualizar `CLAUDE.md` com os comandos reais de build, lint e teste (removendo o "not installed yet"); verificar que cada comando citado roda como escrito (blocked by: 4.2)

## Workflow follow-up

- Decidir se o check de CI vira obrigatório na `develop` (Open Question do `design.md`).
- Arquivar o change com `openspec-archive-change` depois que todas as tasks estiverem marcadas, para criar `openspec/specs/configuration` e `openspec/specs/quality-gate`.
