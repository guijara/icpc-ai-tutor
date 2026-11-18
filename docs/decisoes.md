# Diário de decisões

Arquivo para você editar à mão: ajuste, reabra ou risque decisões conforme o projeto andar. Cada entrada tem a decisão, as alternativas que foram descartadas, o motivo e o status. Registro inicial feito em 16/11/2026, a partir da conversa de planejamento.

---

## Produto

### D01 — Fluxo de trabalho em Git
- **Decisão:** o trabalho acontece na branch `develop`; a `main` não é alterada por enquanto.
- **Motivo:** proteger a `main` até haver algo estável.
- **Status:** decidido.

### D02 — Editorial deixa de ser obrigatório
- **Decisão:** o gabarito fraco do bot são as tags, o rating e o enunciado. Um "motor de raciocínio" liga a técnica das tags ao enunciado.
- **Alternativas:** scraping de editoriais; pedir o editorial ao aluno.
- **Motivo:** o Codeforces bloqueia robôs (403), o LeetCode proíbe scraping nos termos, e muitos problemas não têm editorial.
- **Status:** decidido.

### D03 — Sem scraping; plataformas no MVP
- **Decisão:** Codeforces pela API pública `problemset.problems` (com cache, ~11,5 mil problemas, sem enunciado). LeetCode, AtCoder e Beecrowd: o aluno cola os dados, e o bot avisa disso no aviso de uso.
- **Motivo:** respeitar os termos das plataformas.
- **Em aberto:** a política de scraping do AtCoder não foi confirmada; a AtCoder Problems (API da comunidade) pode dar dificuldade, a verificar.
- **Status:** decidido para o MVP.

### D04 — Sem modo de desistência
- **Decisão:** o bot nunca entrega código aceito. No fim da escada explica a solução em linguagem natural e, se o aluno pedir algo mais concreto, um pseudocódigo curto (nível 4 em diante).
- **Alternativas:** comando "desisto" que entregava a solução completa (previsto no README antigo).
- **Motivo:** evitar que o aluno se sinta tentado a pedir a resposta.
- **Status:** decidido.

### D05 — Comandos e interface
- **Decisão:** só `/problema` e `/dica` (este força +1 nível). O bot responde a toda mensagem dentro da thread. Botões "ajudou" e "não entendi".
- **Alternativas descartadas:** `/debug`, `/teoria`, `/esquecer`.
- **Motivo:** simplicidade. Os dados somem pela regra de 30 dias; um pedido de apagamento antes disso seria manual.
- **Status:** decidido.

### D06 — Idiomas
- **Decisão:** dicas sempre em português; aceita C++ e Python; Java fora.
- **Status:** decidido.

### D07 — Roteador entre conversa e código
- **Decisão:** um roteador (regra barata e, se duvidoso, LLM) separa linguagem natural de código. Conversa em linguagem natural não passa pela análise de código.
- **Motivo:** reduzir custo e tempo, e incentivar o raciocínio abstrato antes do código.
- **Status:** decidido.

### D08 — SLA
- **Decisão:** meta de p95 até 20 s na primeira dica, com teto de 30 s. O bot responde "analisando..." de imediato e depois edita a mensagem.
- **Alternativas:** 10 s com teto de 15 s (README antigo), considerado irreal para 3 chamadas de LLM em sequência.
- **Status:** decidido.

## Pedagogia

### D09 — Escada de dicas
- **Decisão:** 1 entender o problema (só perguntas); 2 direcionamento indireto (sem nomear a técnica); 3 técnica e o porquê (sinais de reconhecimento); 4 aplicação em prosa, com pseudocódigo curto a pedido. Depois do 4, a conversa continua em refinamento.
- **Regras gerais:** reconhecer o que o aluno fez; 1 ou 2 perguntas por resposta; com código, apontar o sintoma e perguntar, sem corrigir linha a linha.
- **Status:** decidido. A redação final dos prompts ainda precisa ser escrita.

### D10 — Quem avança o nível
- **Decisão:** o Tutor decide, ao cumprir o objetivo de saída do nível ou após 2 respostas sem progresso. Nunca pula níveis. `/dica` força +1.
- **Alternativa:** avanço só pelo `/dica`.
- **Status:** decidido; o número "2" pode ser ajustado.

### D11 — Adaptação sem monitor humano
- **Decisão:** o bot é totalmente autônomo. Em sinais de confusão ("não entendi", erros repetidos), ele simplifica ou usa metáfora, sem subir de nível. Tom lúdico só nesses casos.
- **Alternativa descartada:** revisão de análises por um monitor.
- **Status:** decidido.

## Agentes e dados

### D12 — Pesquisador é uma ferramenta
- **Decisão:** deixa de ser um agente com LLM; vira regex no link mais consulta ao cache do Codeforces.
- **Status:** decidido.

### D13 — Análise do problema compartilhada
- **Decisão:** uma análise por problema, salva e reaproveitada, com versão, nível de confiança, técnicas aceitas (lista, não uma só), pistas de reconhecimento e escada pronta. Guarda um resumo próprio, **não o enunciado completo** (direitos autorais). Verificação cruzada (duas execuções) para reduzir erro. Confiança baixa faz o Tutor afirmar menos.
- **Status:** decidido.

### D14 — Revisor e contagem de chamadas
- **Decisão:** Revisor com regra determinística e LLM que melhora a resposta. Chamadas por interação: 3 (código novo), 2 (continuação), +1 na primeira vez de cada problema.
- **Status:** decidido.

### D15 — Estado e banco
- **Decisão:** bot stateless; Supabase com `problems`, `problem_analyses`, `threads`, `messages`, `code_analyses`, `feedback` e `students` (ID do Discord só como HMAC). Trava por thread contra eventos duplicados. Mensagens e códigos somem após 30 dias; ficam as análises e as métricas agregadas.
- **Status:** decidido.

### D16 — RAG
- **Decisão:** fontes: Halim 1 e 2 e cp-algorithms (pelo repositório no GitHub). Corpus e consultas em inglês, com campo "nome em português". Titan Text Embeddings V2 + ChromaDB `PersistentClient`. PDFs e índice fora do Git. O pipeline começa pelo cp-algorithms.
- **Alternativa:** embedding multilíngue local no servidor (descartada: usa RAM e o Titan custa centavos).
- **Em aberto:** idiomas do Titan V2; licença do cp-algorithms (parece CC BY-SA 4.0); você precisa ter cópias legítimas do Halim; Cormen só se a avaliação mostrar lacunas.
- **Status:** decidido.

## Modelos e infraestrutura

### D17 — Provedor de modelos
- **Decisão:** AWS Bedrock com o crédito de US$ 120 (3 meses). Claude Haiku 5.5 para roteador, Tutor, análise de código e Revisor; Claude Sonnet 5.5 para a análise do problema; por perfil de inferência global em `us-east-1`, com prompt caching.
- **Alternativas descartadas:** Gemini via Vertex (créditos do AI Pro incertos), DeepSeek direto (provedor fora do Brasil e sem créditos), Azure for Students (cota de 1 mil tokens por minuto), Nova (indisponível em São Paulo), GPT (caro).
- **Motivo:** os créditos cobrem o Bedrock, e o Haiku 5.5 tem ótimo custo-benefício.
- **Em aberto:** os modelos novos não existem em São Paulo, só por inferência global (dados processados fora do Brasil). Conferir no console os IDs dos perfis e o acesso liberado.
- **Status:** decidido; a avaliação confirma a escolha.

### D18 — Hospedagem
- **Decisão:** EC2 t4g.small (ARM) por 3 meses, com IAM role; depois migrar para o Oracle Cloud Free (ARM).
- **Alternativa:** só Oracle Free desde o início.
- **Motivo:** aprender AWS enquanto há crédito, e ARM nos dois lados evita surpresas na migração.
- **Status:** decidido.

### D19 — Ambientes
- **Decisão:** desenvolvimento no notebook, com bot e projeto Supabase próprios; produção no EC2.
- **Status:** decidido.

### D20 — CI/CD desde o início
- **Decisão:** GitHub Actions. CI em todo PR (`ruff` e testes unitários). CD no merge na `main`: migrations do Supabase (só para frente), deploy por OIDC + Systems Manager, teste de fumaça, reversão pelo commit anterior. Avaliação completa só sob demanda.
- **Alternativa:** deploy manual no MVP.
- **Status:** decidido.

### D21 — Base do projeto
- **Decisão:** `uv`, `ruff`, `pytest`, `pydantic-settings`, estrutura `src/icpc_tutor/{bot,agents,tools,rag,db}`, `evals/`, `scripts/`, `.env.example`.
- **Status:** decidido.

## Qualidade e segurança

### D22 — Avaliação
- **Decisão:** golden dataset de 12 a 15 casos, com fichas montadas a partir de editoriais que o autor vai colar (**adiado**); regras determinísticas e juiz Sonnet 5.5; linha de base com uma única chamada; calibração manual de ~20 resultados; aluno simulado na segunda fase.
- **Status:** decidido; dataset pendente.

### D23 — Segurança
- **Decisão:** anotada para uma fase posterior: limite por aluno e teto de custo; entrada do aluno como dado não confiável; Revisor como barreira; filtro determinístico de saída; minimização de dados e LGPD; segredos com menor privilégio.
- **Status:** adiado.

## Documentação

### D24 — Política dos documentos
- **Decisão:** o repositório é privado, e o README traz o produto, a arquitetura, a infra e os custos. `docs/conceitos.md` e `docs/decisoes.md` são versionados. `docs/plano-do-projeto.md` fica fora do Git (`.gitignore`).
- **Status:** decidido.

---

## Pendências abertas

- IDs dos perfis de inferência global do Haiku 5.5 e do Sonnet 5.5 em `us-east-1`, e acesso liberado.
- Problemas e editoriais do golden dataset.
- Projeto gratuito do Supabase pode ser pausado após uma semana sem uso (conferir).
- Idiomas do Titan V2, licença do cp-algorithms e cópias legítimas do Halim.
- Os 3 meses de crédito da AWS já correm: o primeiro passo de implementação deve ser rápido.
