# Proposal

## Why

O projeto está na fase de especificação, sem código, e o crédito de 3 meses da AWS já está correndo. Antes de qualquer feature, precisamos de uma base em que cada mudança seja validada automaticamente: configuração que falha cedo, testes que rodam sem gastar LLM e um CI que barra PRs quebrados. Sem isso, cada fatia seguinte herda uma base sem prova de que funciona.

Esta é a fatia 1a do Passo 1 (`docs/plano-do-projeto.md` §11), no método 80/20: entregar o fundamental rápido, com testes desde o início.

## What Changes

- Criar o projeto Python 3.11 gerenciado pelo `uv`, com a estrutura `src/icpc_tutor/` contendo apenas o que esta fatia usa.
- Adicionar configuração tipada com `pydantic-settings`, lendo o `.env`, que falha na inicialização com mensagem clara quando falta uma variável obrigatória.
- Versionar um `.env.example` com os nomes das variáveis e nenhum valor real.
- Adicionar um pipeline de CI no GitHub Actions que roda `ruff` e `pytest` em todo PR e em todo push na `develop`.
- Excluir os testes marcados como `llm` por padrão, para que o CI nunca chame um modelo.
- **Nenhum** comportamento de bot é implementado nesta fatia. O bot "Pong", as migrations e o deploy ficam para as fatias 1c a 1f.

Não há mudanças incompatíveis (sem **BREAKING**), porque o repositório não tem código em produção.

## Capabilities

### New Capabilities

- `configuration`: como o sistema carrega e valida suas configurações na inicialização, incluindo a falha antecipada e o contrato do `.env.example`.
- `quality-gate`: quais verificações automáticas são obrigatórias para aceitar uma mudança (lint e testes), em quais eventos rodam e como os testes que chamam LLM são isolados.

### Modified Capabilities

Nenhuma. Não existem specs em `openspec/specs/` ainda.

## Impact

- **Código novo:** `pyproject.toml`, `src/icpc_tutor/` (com o módulo de configuração), `tests/`, `.env.example`.
- **Ferramentas:** `uv`, `ruff`, `pytest`, `pydantic-settings`.
- **CI:** novo workflow em `.github/workflows/`.
- **Git:** o `.gitignore` já cobre `.env` e caches do Python; não precisa de mudança.
- **Custo:** zero. Nenhuma chamada a Bedrock, Supabase ou Discord nesta fatia.
- **Fora de escopo:** bot, banco, deploy, EC2, IAM, qualquer alteração na branch `main`.
