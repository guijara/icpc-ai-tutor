# Spec Delta

## Purpose

Define como o tutor carrega, valida e documenta suas configurações, para que um ambiente mal configurado falhe logo na inicialização e não no meio de uma conversa com o aluno.

## ADDED Requirements

### Requirement: Configuração validada na inicialização
O sistema MUST carregar suas configurações a partir do ambiente e do arquivo `.env` na inicialização, validando tipo e presença de cada valor antes de aceitar qualquer evento. Uma configuração inválida MUST interromper a inicialização.

#### Scenario: Inicialização com configuração completa
- **WHEN** todas as configurações obrigatórias estão presentes e têm o tipo correto
- **THEN** o sistema inicializa e expõe os valores validados para o restante do código

#### Scenario: Configuração obrigatória ausente
- **WHEN** uma configuração obrigatória não está definida no ambiente nem no `.env`
- **THEN** o sistema interrompe a inicialização com erro que nomeia a configuração ausente
- **AND** nenhuma conexão externa é aberta antes da interrupção

#### Scenario: Valor com tipo inválido
- **WHEN** uma configuração está definida, mas não pode ser convertida para o tipo esperado
- **THEN** o sistema interrompe a inicialização com erro que nomeia a configuração e o tipo esperado

### Requirement: Valor padrão explícito para configurações opcionais
O sistema MUST usar um valor padrão documentado para configurações opcionais, e MUST tratar as demais como obrigatórias. Uma configuração opcional sem valor definido MUST assumir o padrão sem gerar erro.

#### Scenario: Configuração opcional omitida
- **WHEN** uma configuração opcional com padrão documentado não está definida
- **THEN** o sistema usa o valor padrão e inicializa normalmente

### Requirement: Segredos nunca aparecem em saídas
O sistema MUST NOT exibir, registrar ou incluir em mensagens de erro o valor de qualquer configuração marcada como segredo. Mensagens de erro MUST citar apenas o nome da configuração.

#### Scenario: Erro envolvendo um segredo
- **WHEN** uma configuração marcada como segredo está ausente ou inválida
- **THEN** a mensagem de erro cita o nome da configuração
- **AND** a mensagem de erro e os logs não contêm qualquer valor de segredo

### Requirement: Arquivo de exemplo versionado sem valores reais
O repositório MUST versionar um arquivo `.env.example` que lista todas as configurações aceitas, com um comentário por linha e nenhum valor real. O arquivo `.env` MUST permanecer fora do controle de versão.

#### Scenario: Novo desenvolvedor configura o ambiente
- **WHEN** o desenvolvedor copia `.env.example` para `.env` e preenche os valores
- **THEN** todas as configurações exigidas pelo sistema estão presentes no arquivo de exemplo

#### Scenario: Verificação de segredos no repositório
- **WHEN** o repositório é verificado antes de um commit
- **THEN** o `.env.example` não contém valores que pareçam chaves, tokens ou senhas
- **AND** o `.env` real está listado no `.gitignore`
