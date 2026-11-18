# ♟️ CodeCoach ICPC — Tutor Autônomo de Maratona de Programação

O **CodeCoach ICPC** é um ecossistema agêntico de tutoria integrado ao Discord, desenvolvido para auxiliar competidores da Maratona de Programação (ICPC/SBC) na universidade.

O sistema utiliza **colaboração multiagente (CrewAI)** e **RAG (Retrieval-Augmented Generation)** para ajudar o aluno a desenvolver raciocínio e pensamento crítico com problemas de maratona, oferecendo dicas pedagógicas sobre algoritmos e estruturas de dados **sem entregar o código da resposta**.

> **Status:** fase de especificação concluída; a implementação ainda não começou. As decisões estão registradas em [`docs/decisoes.md`](docs/decisoes.md) e o mapa de conceitos para estudo em [`docs/conceitos.md`](docs/conceitos.md).

---

## 🧠 Como Funciona o Sistema Multiagente

O aluno abre uma thread com `/problema <link>` e conversa com o bot dentro dela. A cada mensagem, o fluxo é:

```text
 [ Mensagem do aluno ] -> [ Roteador ] -> [ Pesquisador (ferramenta) ] -> [ Análise do problema ]
   (texto ou código)       (conversa ×      (metadados do problema)        (compartilhada e cacheada)
                            código)
                                   |
                                   v
              [ Análise do código ] -> [ Tutor ] -> [ Revisor ] -> [ Resposta na thread ]
               (só se houver código)    (dica do      (barra spoilers
                                         nível certo)  e melhora a dica)
```

1. **Roteador:** separa conversa em linguagem natural de envio de código (C++ ou Python), para não gastar análise de código à toa.
2. **Pesquisador:** ferramenta sem LLM. Extrai a plataforma e o ID do link e consulta o cache da API pública do Codeforces (nome, rating, tags). Nas demais plataformas, o aluno cola o enunciado.
3. **Análise do problema:** um agente que usa as tags, as restrições e o enunciado para decidir a técnica esperada e **por que** ela se aplica. O resultado é salvo e compartilhado entre os alunos.
4. **Análise do código:** inspeciona a complexidade e os casos de borda do código do aluno, só por leitura (o código nunca é executado).
5. **Tutor:** transforma a análise numa dica socrática do nível adequado.
6. **Revisor:** uma regra determinística barra vazamentos (código, solução entregue), e um LLM melhora a resposta quando preciso.

## ✨ Destaques e Funcionalidades

- **Orquestração de agentes com CrewAI**, com papéis, ferramentas customizadas e tarefas sequenciais.
- **Escada de dicas** em 4 níveis, que ensina a *reconhecer* a técnica em problemas futuros.
- **Análise do problema compartilhada:** uma análise por problema, reaproveitada por todos os alunos, com nível de confiança.
- **RAG com fontes de referência:** Halim (Competitive Programming 1 e 2) e cp-algorithms, indexados com resumos estruturados.
- **Bot de Discord com threads isoladas** por aluno e problema, e memória guardada em banco, não em RAM.
- **Avaliação contínua** contra um golden dataset, com regras determinísticas e um juiz LLM.

---

## Fase 1 do Desenvolvimento → Documento de Especificação

### 1. Visão Geral do Produto

**Objetivo:** um agente tutor para o Discord que ajude universitários a desenvolverem raciocínio crítico em algoritmos de maratona.

**Público-alvo:** estudantes de nível iniciante e intermediário (estruturas de dados, programação dinâmica, grafos, matemática etc.).

**Filosofia pedagógica (scaffolding):** o bot **nunca entrega código aceito**. Ele guia por dicas progressivas. Ao fim da escada pode explicar a solução em linguagem natural e, se o aluno pedir algo mais concreto, um pseudocódigo curto. Não existe mais comando de desistência.

### 2. Interação e Interface

- **Plataforma:** Discord, com **Pycord**.
- **Comandos:** apenas `/problema <link>` (abre a thread de estudo) e `/dica` (força o avanço de um nível). Dentro da thread, o bot responde a todas as mensagens.
- **Feedback:** botões "ajudou" e "não entendi" nas respostas. O "não entendi" faz o Tutor simplificar ou usar uma metáfora, sem subir de nível.
- **Isolamento de sessão:** uma thread por dúvida, com contexto e memória separados por aluno e problema.
- **Entradas aceitas:** texto natural, links de juízes online e código em **C++ ou Python** (Java fora do escopo). As dicas são sempre em **português**.
- **Plataformas:** no MVP, Codeforces (metadados pela API pública). Para LeetCode, AtCoder e Beecrowd, o aluno envia o enunciado e os dados, e o bot avisa disso. Não há scraping: o LeetCode proíbe nos termos, o Codeforces bloqueia robôs e a política do AtCoder é incerta.

### 3. Escada de Dicas (algoritmo de raciocínio)

| Nível | Foco | O que o bot faz |
|---|---|---|
| 1 | Entender o problema | Só perguntas: entrada e saída, limites, complexidade alvo, exemplo à mão, casos de borda. |
| 2 | Direcionamento indireto | Propriedades dos dados, analogias, "o que muda se...", sem nomear a técnica. |
| 3 | Técnica e o porquê | Nomeia a técnica e os sinais do enunciado e das restrições que a indicam, com um problema clássico análogo. |
| 4 | Aplicação em prosa | Passos numerados e complexidade. Pseudocódigo curto só a pedido. Depois, conversa de refinamento. |

**Regras gerais:**
- Reconhecer o que o aluno já fez ou entendeu; no máximo 1 ou 2 perguntas por resposta; respostas curtas.
- Com código enviado, apontar o sintoma (complexidade, caso de borda) e perguntar sobre o trecho, sem corrigir linha a linha.
- Metáfora e tom lúdico só quando o aluno der sinais de confusão.
- O **Tutor decide** quando avançar: ao cumprir o objetivo de saída do nível ou após duas respostas sem progresso. Nunca pula níveis. O `/dica` força +1.

### 4. Fontes de Dados e Ferramentas

- **Metadados de problemas:** API pública do Codeforces (`problemset.problems`), com cache. Traz nome, rating e tags, mas não o enunciado nem o editorial.
- **Editorial:** não é mais obrigatório. O gabarito fraco do bot são as tags, o rating e o enunciado.
- **Base de conhecimento:** Halim 1 e 2 e cp-algorithms (pelo repositório no GitHub). Os PDFs e o índice ficam fora do Git.
- **Análise de código:** feita só por leitura do LLM, sem execução e sem sandbox.

### 5. Restrições e Métricas

- **SLA:** meta de p95 até **20 s** na primeira dica, com teto de **30 s**. O bot responde "analisando..." de imediato e depois edita a mensagem.
- **Qualidade:** golden dataset de problemas, regras determinísticas, juiz LLM, feedback dos alunos, Taxa de Resolução Autônoma e Custo por Sessão.

---

## Fase 2 do Desenvolvimento → Design e Arquitetura

**Arquitetura base:** pipeline multiagente sequencial (padrão ReWOO: planejar, agir, sintetizar), sem sandbox e com validação por análise estática.

**Agentes e ferramentas:**
- **Pesquisador:** ferramenta sem LLM (regex no link + cache do Codeforces).
- **Analista do problema:** técnicas aceitas, pistas de reconhecimento, escada de dicas pronta e nível de confiança. A análise é versionada e guarda um resumo próprio, **não o enunciado completo**. Quando não há tags (fora do Codeforces), a confiança é menor e o Tutor afirma menos.
- **Analista de código:** complexidade e casos de borda, por envio.
- **Tutor:** dica no nível certo, com adaptação a sinais de confusão.
- **Revisor:** regra determinística (sem blocos de código nem solução completa) e, se preciso, LLM que melhora a resposta.
- **Custo em chamadas por interação:** 3 com código novo, 2 numa continuação, e +1 na primeira vez que um problema aparece (a análise do problema fica no cache).

**RAG:** indexação agêntica (um LLM resume cada seção das fontes com campos fixos: técnica, quando usar, sinais de reconhecimento, complexidade, armadilhas). O corpus e as consultas são em inglês, com um campo "nome em português". A consulta é gerada pela análise do problema, e a busca no bot é semântica simples. Alimenta o Tutor (níveis 3 e 4) e o Analista.

**Estado:** o bot é **stateless**. O histórico vive no Supabase (PostgreSQL), com as tabelas `problems`, `problem_analyses`, `threads`, `messages`, `code_analyses`, `feedback` e `students` (ID do Discord guardado só como HMAC). Há uma trava por thread contra eventos duplicados. Mensagens e códigos são apagados após **30 dias**.

---

## Fase 3 do Desenvolvimento → Frameworks e Ferramentas

- **Linguagem:** Python 3.11, com `uv` (ambiente e dependências), `ruff` (lint e formatação) e `pytest`.
- **Configuração:** `pydantic-settings` lendo o `.env`, com validação na inicialização e um `.env.example` versionado.
- **Orquestração:** CrewAI (sequencial) com LiteLLM para o roteamento de modelos. O CrewAI roda fora do event loop do bot.
- **Interface:** Pycord (slash commands e threads nativos).
- **Banco relacional:** Supabase (PostgreSQL), com migrations só para frente.
- **Banco vetorial:** ChromaDB em modo `PersistentClient`, em disco local.
- **Modelos (AWS Bedrock):** Claude **Haiku 5.5** (roteador, Tutor, análise de código, Revisor) e Claude **Sonnet 5.5** (análise do problema), por perfil de inferência global em `us-east-1`, com prompt caching. Embeddings: **Titan Text Embeddings V2**.
- **Estrutura prevista:** `src/icpc_tutor/{bot,agents,tools,rag,db}`, `evals/` e `scripts/`.

### Infraestrutura e CI/CD

- **Hospedagem:** EC2 **t4g.small** (ARM) durante os 3 meses de crédito, com IAM role para o Bedrock (sem chave guardada). Depois, migração para o Oracle Cloud Free (também ARM).
- **Ambientes:** desenvolvimento (notebook, com bot e projeto Supabase próprios) e produção (EC2).
- **Operação:** serviço `systemd`, alerta por webhook no Discord, AWS Budgets e teto de custo dentro do bot.
- **CI/CD (GitHub Actions), desde o início:**
  - CI em todo PR: `ruff` e testes unitários, sem chamar LLM.
  - CD no merge na `main`: migrations do Supabase, deploy no EC2 por OIDC + AWS Systems Manager (sem porta aberta), teste de fumaça e reversão pelo commit anterior.
  - Avaliação completa (que chama LLM) só sob demanda.

### Custos

- **Crédito:** US$ 120 do free tier da AWS, válidos por 3 meses, cobrindo Bedrock (inclusive modelos de terceiros).
- **Estimativa:** cerca de US$ 0,002 por interação no Haiku 5.5 (premissa: ~9 mil tokens de entrada e ~1,5 mil de saída), e ~US$ 0,04 por análise de problema no Sonnet 5.5. Algo como 3 mil interações por mês cabem em ~US$ 5.
- **Depois dos créditos:** custo próprio na faixa de US$ 5 por mês, e o Oracle Free evita o custo de hospedagem. DeepSeek direto fica como alternativa.
- **Privacidade:** a inferência global pode processar os dados fora do Brasil. O aviso de uso do bot informa isso aos alunos.

---

## 🧪 Avaliação

- **Golden dataset** de 12 a 15 casos (problemas com tags, entradas de aluno em linguagem natural e em código com bug, e a resposta esperada), montado a partir de editoriais selecionados.
- **Regras determinísticas** (sem código na resposta, em português, técnica nomeada só do nível 3 em diante) e **juiz LLM** (Sonnet 5.5) com rubrica.
- **Linha de base:** uma única chamada de LLM, para provar que a crew compensa a complexidade.
- **Métricas:** latência (p95), custo por interação, Taxa de Resolução Autônoma.
- **Segunda fase:** aluno simulado (um LLM com personas) para testar a escada de dicas em conversas de vários turnos.

## 🔒 Segurança e Privacidade (planejado)

Limite de uso por aluno e teto de custo; tudo que vem do aluno tratado como dado não confiável (prompt injection); Revisor como barreira final; filtro determinístico de saída; minimização de dados (sem nome nem ID do Discord enviados ao modelo), retenção de 30 dias e conformidade com a LGPD; segredos e chaves com o menor privilégio possível.

## 🗺️ Roadmap

1. **Fundação, esqueleto e CI/CD:** bot "Pong" com `defer` e thread, migrations do Supabase, EC2 com IAM role e uma chamada de teste ao Haiku 5.5 (valida crédito, cota e latência).
2. **Avaliação:** harness, regras determinísticas e linha de base.
3. **Ferramentas:** Pesquisador (cache do Codeforces) e roteador.
4. **Agentes e tarefas** (CrewAI) e **ingestão do RAG**, em paralelo.
5. **MVP em fatias:** `/problema` com thread e Supabase, Tutor único, crew completa, botões e limites.

## 📦 Configuração (planejada)

O código ainda não existe; este é o desenho previsto.

```bash
git clone https://github.com/guijara/icpc-ai-tutor.git
cd icpc-ai-tutor
uv sync            # instala as dependências
cp .env.example .env
```

Variáveis de ambiente previstas: `DISCORD_BOT_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `AWS_REGION`, `CHROMADB_PATH` (padrão `./data/chromadb`) e a chave secreta do HMAC dos IDs. No EC2, o Bedrock é acessado pela IAM role, sem chaves.

## 🛠️ Tech Stack

- **IA e agentes:** Python, CrewAI, LiteLLM, AWS Bedrock (Claude Haiku 5.5 e Sonnet 5.5, Titan Embeddings V2).
- **Dados:** Supabase (PostgreSQL), ChromaDB.
- **Interface:** Pycord (Discord).
- **Qualidade e entrega:** uv, ruff, pytest, pydantic-settings, GitHub Actions.
- **Infra:** AWS EC2 e Systems Manager, depois Oracle Cloud Free.

---

## 🤝 Impacto Educacional

O projeto atua diretamente no projeto de extensão da Universidade Federal de Mato Grosso (UFMT), reduzindo gargalos de atendimento aos alunos iniciantes e criando um ambiente seguro para o aprendizado prático e autônomo de estruturas de dados avançadas.

---

## 👨‍💻 Autor

Desenvolvido por **Guilherme Jara**  
[LinkedIn](https://linkedin.com/in/guilhermejara) | [GitHub](https://github.com/guijara)
