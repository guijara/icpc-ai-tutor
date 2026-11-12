# ♟️ CodeCoach ICPC — Tutor Autônomo de Maratona de Programação

O **CodeCoach ICPC** é um ecossistema agêntico de tutoria em produção integrado ao Discord, desenvolvido para auxiliar competidores da Maratona de Programação (ICPC/SBC) na universidade. 

O sistema utiliza **colaboração multiagente (CrewAI)** e **RAG (Retrieval-Augmented Generation)** para auxiliar o aluno a desenvolver raciocínio e pensamento crítico de maneira aplicada com os problemas da maratona, oferecendo dicas pedagógicas sobre algoritmos e estruturas de dados sem entregar a resposta pronta.

---

## 🧠 Como Funciona o Sistema Multiagente

O bot orquestra agentes autônomos que debatem internamente antes de responder ao aluno no Discord:

```text
 [ Aluno envia prompt ] -> [ Agente de Pesquisa ] -> [ Agente de código ] -> [ Agente Pedagogo ] -> [ Resposta ]
   (TLE / WA / RTE)       (Verifica qual o exercício em questão)  (Base Algorítmica)  (Gera a resposta)
```
---

## ✨ Destaques e Funcionalidades

- **Orquestração de Agentes com CrewAI:** Atribuição de papéis, ferramentas customizadas e delegação sequencial de tarefas.
- **RAG sem Alucinações:** Ingestão de materiais de referência em banco vetorial, garantindo precisão teórica nas explicações.
- **Aumento de Produtividade com Claude Code:** Desenvolvimento acelerado da base de agentes e engenharia de prompts avançada.
- **Bot em Produção para Discord:** Interface fluida onde o usuário já estuda e interage com a comunidade.

---

## Fase 1 do Desenvolvimento -> Documento de Especificação

### 1. Visão Geral do Produto

Objetivo: Desenvolver um agente tutor para o Discord que auxilie universitários a desenvolverem raciocínio crítico em algoritmos de maratona (ICPC/SBC).

Público-Alvo: Estudantes de nível iniciante e intermediário focados em estruturas de dados, programação dinâmica, grafos, matemática, etc.

Filosofia Pedagógica: Abordagem de Scaffolding (andaime). O agente nunca entrega o código final ou a resposta direta imediatamente. Ele guia o aluno através de dicas progressivas conceituais e de lógica.

Modo Solucionador: O agente possui um "botão de emergência" (ex: um comando de desistência explícito) onde altera seu estado para fornecer a resolução completa caso o aluno trave totalmente.

### 2. Interação e Interface (I/O)

Plataforma: Discord.

Gatilho de Ação: O agente operará de forma determinística via Slash Commands (ex: /teoria, /debug, /dica).

Isolamento de Sessão: A interação ocorrerá estritamente dentro de Threads específicas criadas para cada dúvida, isolando o contexto e a memória da conversa por aluno/problema.

Entradas Suportadas: Texto natural, links de juízes online (URI/Beecrowd, Codeforces) e blocos de código-fonte (snippets curtos).

### 3. Fontes de Dados e Ferramentas

Buscador Web / Scraper: Ferramenta ativa para buscar o problema online e, obrigatoriamente, recuperar o Editorial (Ground Truth) correspondente antes de iniciar a tutoria.

Base de Conhecimento: Ingestão de literatura clássica de maratona (ex: Competitive Programming do Halim) para embasamento de explicações teóricas.

Análise de Código: Feita exclusivamente via análise estática do LLM comparada ao editorial (sem execução em terminal/sandbox).

### 4. Restrições e Métricas

Infraestrutura: APIs comerciais de baixo custo focadas em código (OpenAI gpt-4o-mini ou DeepSeek V3/Coder).

Performance (SLA): Tempo de resposta das interações abaixo de 10 segundos (teto rígido de 15 segundos).

Avaliação de Qualidade: Validação contra um Golden Dataset de problemas e logs de conversas, feedback direto dos alunos, medição da Taxa de Resolução Autônoma e Custo por Sessão.

---

## Fase 2 do Desenvolvimento -> Design e Arquitetura

Arquitetura Base: Sistema Multi-Agente Horizontal (Sequencial) sem execução de código (sandbox), com validação via Análise Estática. Padrão baseado em ReWoo (Planejamento > Ação > Síntese).

Agentes (CrewAI):

Pesquisador: Extrai problema da web e busca o Editorial (Gabarito Oculto).

Analista de Código: Inspeciona sintaxe e valida a complexidade (Big-O) do código do aluno em relação ao Editorial.

Tutor (Comunicador): Gera a resposta com didática de Scaffolding (não dá resposta direta).

Revisor (Reflection): Avalia a saída do Tutor para garantir que os limites pedagógicos não foram violados antes de enviar ao Discord.

RAG (Teoria): Processo de indexação usando RAG Agêntico (LLM estrutura os resumos dos PDFs antes do armazenamento). No fluxo do bot, ocorre apenas busca semântica simples (Retrieve).

Infraestrutura e UX (Discord): Uso de Slash Commands para invocar agentes e criação de Threads dedicadas (interface Discord) para isolar o histórico daquela tutoria.

Gerenciamento de Estado: Arquitetura Stateless (sem estado em RAM). A memória da conversa será gerenciada de forma externa em banco de dados relacional para resiliência. Modelos geridos via LiteLLM para otimização de custo.

---

## Fase 3 do Desenvolvimento -> Frameworks e Ferramentas

- Linguagem: Python.
- Orquestração de Agentes: CrewAI (Arquitetura Sequencial) integrado com LiteLLM para roteamento de APIs de baixo custo (foco em DeepSeek).
- Integração com Interface: Pycord, escolhido pela facilidade nativa em lidar com Slash Commands e gerenciamento de Threads do Discord.
- Banco de Dados Relacional (Memória/Sessões): Supabase (PostgreSQL). Atuará como a fonte da verdade para o histórico das Threads, garantindo que o bot Python seja 100% Stateless (resiliente a falhas e reinicializações).
- Banco de Dados Vetorial (RAG): ChromaDB rodando localmente com o modo PersistentClient (persistência em disco/volume) para armazenar os embeddings dos livros sem custos recorrentes de nuvem.


## 🛠️ Tech Stack

- **Orquestração de IA:** Python, CrewAI, Anthropic Claude Code / OpenAI GPT-4.
- **Armazenamento Vetorial (RAG):** ChromaDB.
- **Integração & Interface:** Pycord.

---
## 🤝 Impacto Educacional

O projeto atua diretamente no projeto de extensão da Universidade Federal de Mato Grosso (UFMT), reduzindo gargalos de atendimento aos alunos iniciantes e criando um ambiente seguro para o aprendizado prático e autônomo de estruturas de dados avançadas.

---

## 👨‍💻 Autor
Guilherme Jara

Desenvolvido por **Guilherme Jara**  
[LinkedIn](https://linkedin.com/in/guilhermejara) | [GitHub](https://github.com/guijara)
