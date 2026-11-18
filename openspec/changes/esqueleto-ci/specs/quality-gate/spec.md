# Spec Delta

## Purpose

Define as verificações automáticas que toda mudança precisa passar antes de entrar na `develop`, e o isolamento dos testes que chamam modelos de linguagem, para que o CI seja barato, rápido e não dependa de credenciais.

## ADDED Requirements

### Requirement: CI executa lint e testes em PRs e na develop
O sistema MUST executar a verificação de lint e a suíte de testes unitários e de integração em todo pull request aberto ou atualizado, e em todo push na branch `develop`. O resultado MUST ser reportado como aprovado ou reprovado no próprio PR.

#### Scenario: PR aberto com mudanças válidas
- **WHEN** um pull request é aberto contra a `develop` e não há erros de lint nem falhas nos testes
- **THEN** a verificação de CI é reportada como aprovada no PR

#### Scenario: PR com falha de teste
- **WHEN** um pull request contém um teste que falha
- **THEN** a verificação de CI é reportada como reprovada
- **AND** o relatório identifica o teste que falhou

#### Scenario: Push na develop
- **WHEN** um commit é enviado para a branch `develop`
- **THEN** o CI executa as mesmas verificações de um pull request

### Requirement: Testes do CI não dependem de credenciais externas
O CI MUST executar a suíte padrão sem qualquer segredo configurado no repositório. Os testes padrão MUST NOT chamar modelos de linguagem, o Discord, o Supabase ou a AWS.

#### Scenario: Execução sem segredos
- **WHEN** o CI roda em um fork ou em um ambiente sem nenhum segredo definido
- **THEN** a suíte padrão executa até o fim sem erro de autenticação

#### Scenario: Chamada indevida a serviço externo
- **WHEN** um teste padrão tenta abrir uma conexão com um serviço externo
- **THEN** o teste falha antes de enviar qualquer requisição

### Requirement: Testes que chamam LLM são opt-in
Os testes que chamam modelos de linguagem MUST ser marcados como `llm` e MUST NOT ser executados por padrão nem pelo CI. Eles MUST executar apenas quando solicitados explicitamente.

#### Scenario: Execução padrão da suíte
- **WHEN** a suíte é executada sem seleção de marcadores
- **THEN** nenhum teste marcado como `llm` é executado

#### Scenario: Execução explícita dos testes com LLM
- **WHEN** o desenvolvedor solicita os testes marcados como `llm` de forma explícita
- **THEN** somente os testes marcados como `llm` são executados
