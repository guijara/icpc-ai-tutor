# Design

## Context

O repositório tem só documentação (`README.md`, `docs/`) e a configuração do OpenSpec. Não há código, `pyproject.toml`, testes nem workflows. O `.gitignore` já cobre `.env`, `.venv/`, caches do Python e `data/`.

O README (Fase 3) fixa Python 3.11, `uv`, `ruff`, `pytest` e `pydantic-settings`. A D19 separa ambiente de desenvolvimento (notebook) e de produção (EC2). Esta fatia precisa provar esses fundamentos antes de qualquer feature. Ver `proposal.md` para a motivação.

## Goals / Non-Goals

**Goals:**
- Um comando único reproduz o ambiente (`uv sync --locked`) no notebook, no CI e depois no EC2.
- Configuração validada na inicialização, com falha antecipada e legível.
- Suíte padrão roda em qualquer máquina, sem credenciais e sem tráfego de rede.
- Um PR com lint quebrado ou teste quebrado aparece como reprovado.

**Non-Goals:**
- Nenhum segredo real é cadastrado nesta fatia. A convenção para segredos é definida agora e usada a partir da fatia 1b/1c.
- Camada de integração com banco fica para a fatia 1d, quando existir uma migration para testar.
- Sem bot, sem Discord, sem chamada a LLM.
- Sem deploy nem workflow de CD.

## Decisions

### Python 3.11 fixado pelo `uv`
O projeto declara `requires-python = "==3.11.*"` e um arquivo `.python-version` com `3.11`. O `uv` instala essa versão à parte, então o Python 3.14 do notebook não entra no caminho.
- **Alternativa descartada:** usar o Python do sistema. Isso faria o notebook, o CI e o EC2 rodarem versões diferentes, e o EC2 precisa ser estável nos 3 meses de crédito.

### Configuração como objeto, não como variável global
Um `Settings` (`pydantic-settings`) em `src/icpc_tutor/config.py`, obtido por uma função `get_settings()` que lê o ambiente na primeira chamada e guarda o resultado.
- **Por que:** a validação roda quando o código pede a configuração, não no import. Assim os testes injetam valores com `monkeypatch` e nenhum teste depende do `.env` real.
- **Alternativa descartada:** instância global criada no import. Ela quebra qualquer `import` quando faltar uma variável, inclusive em ferramentas como o `pytest` e o `ruff`.

### Duas configurações concretas nesta fatia
- `APP_ENV`: obrigatória, com valores `dev` ou `prod`. Não tem padrão, para que ninguém suba o código em produção por esquecimento (D19).
- `LOG_LEVEL`: opcional, padrão `INFO`. Serve para exercitar o caminho de padrão documentado.
- **Decisão minha, pode trocar:** os nomes e os valores. Se preferir outro nome, muda só o `config.py`, o `.env.example` e os testes.

### Segredos por tipo: `SecretStr`
Qualquer campo de segredo usa `SecretStr`. Assim `repr`, logs e mensagens de erro mostram `**********`, e o valor só sai com `.get_secret_value()`. A convenção fica testada com um modelo de teste dentro da suíte, porque ainda não existe segredo real.

### Marcador `llm` excluído por padrão
Os testes que chamam modelos recebem o marcador `llm`. A configuração de `pytest` exclui esse marcador por padrão, e o desenvolvedor o inclui com `-m llm`.
- **Alternativa descartada:** pular o teste com uma variável de ambiente. É fácil esquecer de ativá-la, e um teste com LLM rodaria por engano no CI.

### Bloqueio de rede nos testes padrão
Uma fixture `autouse` em `tests/conftest.py` substitui a conexão de socket por uma função que levanta erro. Os testes marcados como `llm` recebem uma exceção explícita, porque precisam de rede.
- **Alternativa descartada:** o pacote `pytest-socket`. Funciona igual, mas adiciona uma dependência para ~10 linhas de código.

### Testes sem camada de integração
A única pasta de testes nesta fatia é `tests/unit/`. A integração com Postgres entra na fatia 1d, junto com a primeira migration.

### Um workflow de CI com dois gatilhos
`.github/workflows/ci.yml` roda em `pull_request` (qualquer branch de destino) e em `push` para `develop`. Os passos são: `uv sync --locked`, `ruff check`, `ruff format --check` e `pytest`. Nenhum passo recebe segredo.
- **Por que `--locked`:** falha o CI se o `pyproject.toml` e o `uv.lock` divergirem, em vez de resolver versões novas em silêncio.
- **Push na `main`** fica de fora. Ele é do CD da fatia 1f.

## Risks / Trade-offs

- **[`APP_ENV` padrão ausente pode incomodar no dia a dia]** → é o preço de não subir em produção por engano. O `.env` do notebook define `APP_ENV=dev` uma vez.
- **[Bloqueio de socket derruba uma biblioteca que faz rede no import]** → o erro aparece cedo, no teste que a importa. Nesta fatia não há dependência com essa característica. Se surgir, a fixture aceita uma lista de exceções.
- **[Lockfile desatualizado]** → `--locked` quebra o CI, e a correção é rodar `uv lock` e commitar. Isso é intencional.
- **[O CI reprova um PR, mas não impede o merge]** → a spec pede só o relatório. Bloquear o merge exige regra de proteção na `develop`, que é uma configuração manual no GitHub. Ver Open Questions.

## Migration Plan

Não há migração de dados. A implantação é um commit na `develop` com o workflow novo.

Rollback: reverter o commit. O workflow deixa de existir e nada mais depende dele.

Ordem de execução: lockfile e `pyproject.toml` → `config.py` e testes → `.env.example` → workflow. O workflow só é validado de verdade quando o primeiro PR com essas mudanças roda no GitHub.

## Open Questions

- Tornar o check do CI obrigatório na `develop` (bloqueando o merge com check vermelho)? É uma escolha sua no GitHub e pode ser feita depois do primeiro workflow verde, sem mudar a spec.
