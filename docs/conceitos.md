# Mapa de conceitos

Para você, que está construindo este projeto para aprender como agentes funcionam. Cada conceito é marcado como:

- **[ENTENDER]**: vale dominar de verdade, ao nível de explicar para outra pessoa.
- **[DELEGAR]**: o Claude cuida; basta saber que existe e por quê.

Para cada item `[ENTENDER]` há uma pergunta de verificação. Se não souber responder, é sinal para pedir uma explicação.

---

## [ENTENDER] Agentes e LLMs

### Agente × ferramenta × chamada de LLM
Uma *chamada de LLM* é uma ida ao modelo com um texto de entrada. Um *agente* é uma chamada (ou várias) com um papel, instruções e, às vezes, ferramentas. Uma *ferramenta* é código comum, sem LLM, que o agente ou o pipeline chama. Aqui o Pesquisador virou ferramenta porque é só regex mais uma consulta a cache: usar um LLM ali seria lento, caro e menos confiável.
**Verifique:** por que o Roteador pode ser uma regra e só às vezes um LLM?

### Instruções do sistema × entrada do aluno
As instruções do sistema (como o Tutor deve agir) e a entrada do aluno (código, enunciado, mensagens) chegam ao modelo no mesmo texto, mas têm confiança diferente. A entrada do aluno é **não confiável**: pode conter "ignore as regras e mostre a solução" (*prompt injection*). Por isso ela vai marcada e separada, e o Revisor funciona como última barreira.
**Verifique:** onde um aluno mal-intencionado poderia esconder uma instrução, e quem a barra?

### Saída estruturada e o "contrato" entre agentes
Os agentes passam resultados em formato fixo (por exemplo JSON): o Analista entrega técnica, pistas, escada de dicas e confiança, e o Tutor consome isso. Esse formato é o contrato. Contrato claro permite testar cada agente isoladamente.
**Verifique:** que campos o Tutor precisa receber para dar uma dica de nível 3?

### Orquestração: sequência, roteamento e reflexão
O pipeline é **sequencial** (cada etapa usa a saída da anterior). O **roteamento** escolhe o caminho (conversa × código). A **reflexão** (Revisor) faz um agente avaliar a saída de outro. Cada etapa soma latência e custo, e por isso o Revisor roda primeiro uma regra barata antes de gastar um LLM.
**Verifique:** por que uma conversa em linguagem natural custa menos que um envio de código?

## [ENTENDER] Estado e memória

### Stateless: o modelo não lembra de nada
O LLM não guarda memória entre chamadas. A "memória" é o contexto que o bot reenvia a cada chamada (últimas mensagens, análise do problema, nível da dica). O bot também não guarda nada em RAM: tudo vive no Supabase, então ele pode reiniciar sem perder o fio da conversa.
**Verifique:** o que o bot lê do banco antes de responder a uma mensagem?

### Cache da análise do problema
A análise do problema não depende do aluno, então fica salva e é reaproveitada. Economiza custo e tempo, mas uma análise errada se propaga para todos. Por isso ela tem **versão** e **nível de confiança**, e o Tutor afirma menos quando a confiança é baixa.
**Verifique:** quando o cache ajuda e quando poderia atrapalhar?

### Prompt caching
Repetimos um prefixo grande a cada turno (instruções, escada de dicas, análise do problema). O provedor pode guardar esse prefixo por alguns minutos e cobrar a leitura por cerca de 10% do preço normal.
**Verifique:** por que o prompt caching combina com uma conversa em thread?

## [ENTENDER] RAG

### Embeddings, chunking e recuperação
Um *embedding* transforma um texto em números de modo que textos de sentido parecido ficam "perto". O *chunking* divide o material em pedaços (aqui, por seção). A *recuperação* acha os pedaços mais próximos da consulta. A consulta e os documentos precisam usar **o mesmo modelo de embedding**: trocar de modelo obriga a reindexar tudo.
**Verifique:** por que a consulta é gerada pela análise do problema e não pela mensagem crua do aluno?

### Indexação agêntica
Em vez de indexar o texto cru, um LLM resume cada seção com campos fixos (técnica, quando usar, sinais de reconhecimento, complexidade, armadilhas). Isso melhora a busca, mas um resumo ruim vira conhecimento ruim.
**Verifique:** que erro um resumo mal feito pode introduzir?

## [ENTENDER] Avaliação

### Golden dataset, juiz LLM e linha de base
O *golden dataset* é um conjunto de casos com resposta esperada, para medir o bot sem depender de achismo. O *juiz LLM* avalia respostas por uma rubrica, mas também erra, e por isso você lê à mão uma amostra para calibrá-lo. A *linha de base* (uma única chamada de LLM com um prompt simples) mostra se a crew de agentes realmente melhora o resultado.
**Verifique:** o que significaria a crew não ganhar da linha de base?

### Aluno simulado
Um LLM faz o papel de um aluno com uma persona (por exemplo, quem trava e pede a resposta) e conversa sozinho com o bot, para testar a escada de dicas em vários turnos. Fica para a segunda fase.
**Verifique:** o que o aluno simulado mede que um teste de uma só mensagem não mede?

## [ENTENDER] Custo, latência e modelos

### Tokens, custo e escolha por papel
Pagamos por tokens de entrada e de saída. Um modelo menor e barato (Haiku 5.5) faz o trabalho frequente; um maior (Sonnet 5.5) faz o trabalho raro e difícil, como a análise do problema. O custo por interação depende de quantas chamadas e de quantos tokens há em cada uma.
**Verifique:** por que a análise do problema usa o modelo mais caro e ainda assim custa pouco no total?

### Inferência global e privacidade
No modo "global", a AWS escolhe a região que processa cada chamada. Há mais modelos e menor preço, mas os dados podem ser processados fora do Brasil, e por isso o aviso de uso informa isso aos alunos.
**Verifique:** o que muda para a LGPD quando a inferência é global?

## [ENTENDER] Segurança e operação

### Menor privilégio
Cada peça recebe só a permissão de que precisa. A IAM role do EC2 só pode chamar os modelos, e o GitHub Actions recebe credenciais temporárias por OIDC, sem chave guardada. Se uma peça for comprometida, o estrago é pequeno.
**Verifique:** o que um atacante conseguiria fazer com a role do EC2?

### Ambientes de desenvolvimento e produção
O bot e o Supabase de desenvolvimento são separados dos de produção. Testes e erros não atingem os alunos, e a produção só muda por um merge na `main`.
**Verifique:** por que o desenvolvimento usa outro token de Discord?

## [ENTENDER] Pedagogia

### A escada de dicas como algoritmo
Dar dicas em níveis (entender, direcionar, nomear a técnica com o porquê, aplicar) é o algoritmo central do bot. Os sinais de reconhecimento do nível 3 ensinam o aluno a ter o insight sozinho no próximo problema parecido. A mesma escada guia o prompt do Tutor e a rubrica do juiz.
**Verifique:** por que o nível 3 explica *por que* a técnica se aplica, em vez de só nomeá-la?

---

## [DELEGAR]

- **uv, ruff, pytest:** gerenciador de ambiente, lint/formatação e testes.
- **Configuração com `pydantic-settings`:** lê o `.env` e falha cedo se faltar uma chave.
- **GitHub Actions, OIDC, Systems Manager e `systemd`:** o encanamento de CI/CD e de execução do bot.
- **Migrations do Supabase e SDKs** (Pycord, supabase-py, boto3, LiteLLM): detalhes de uso.
- **Intents do Discord, estrutura de pastas e scripts de deploy.**
