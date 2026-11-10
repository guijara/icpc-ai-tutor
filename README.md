# ♟️ ICPC AI Tutor — Tutor Autônomo de Maratona de Programação

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-red.svg)](https://www.crewai.com/)
[![Discord.py](https://img.shields.io/badge/Discord.py-Bot-5865F2.svg)](https://discordpy.readthedocs.io/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-AI%20Productivity-lightgrey.svg)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

O **CodeCoach ICPC** é um ecossistema agêntico de tutoria em produção integrado ao Discord, desenvolvido para auxiliar competidores da Maratona de Programação (ICPC/SBC) na universidade. 

O sistema utiliza **colaboração multiagente (CrewAI)** e **RAG (Retrieval-Augmented Generation)** para analisar códigos com erros (como *Time Limit Exceeded* ou *Wrong Answer*), oferecendo dicas pedagógicas sobre algoritmos e estruturas de dados sem entregar a resposta pronta.

---

## 🧠 Como Funciona a Tripulação (Crew)

O bot orquestra agentes autônomos que debatem internamente antes de responder ao aluno no Discord:

```text
 [ Aluno cola código ] -> [ Agente Diagnóstico ] -> [ RAG Vetorial ] -> [ Agente Pedagogo ] -> [ Dica no Discord ]
   (TLE / WA / RTE)       (Análise de Complexidade)  (Base Algorítmica)  (Geração sem Spoiler)
```

1. **Especialista em Algoritmos (Diagnóstico):** Avalia a complexidade assintótica do código enviado ($O(N^2)$, $O(N \log N)$) e identifica o gargalo lógico.
2. **Base Vetorial RAG (Recuperação):** Consulta materiais acadêmicos, técnicas de maratona (Busca Binária, Programação Dinâmica, Grafos) e documentações.
3. **Pedagogo Code Coach (Sintetizador):** Converte a análise técnica em uma orientação socrática, fazendo perguntas e dando pistas graduais para estimular o aprendizado do aluno.

---

## ✨ Destaques e Funcionalidades

- **Orquestração de Agentes com CrewAI:** Atribuição de papéis, ferramentas customizadas e delegação sequencial de tarefas.
- **RAG sem Alucinações:** Ingestão de materiais de referência em banco vetorial, garantindo precisão teórica nas explicações.
- **Aumento de Produtividade com Claude Code:** Desenvolvimento acelerado da base de agentes e engenharia de prompts avançada.
- **Bot em Produção para Discord:** Interface fluida onde o usuário já estuda e interage com a comunidade.

---

## Documento de Especificação

1. Visão Geral do Produto

Objetivo: Desenvolver um agente tutor para o Discord que auxilie universitários a desenvolverem raciocínio crítico em algoritmos de maratona (ICPC/SBC).

Público-Alvo: Estudantes de nível iniciante e intermediário focados em estruturas de dados, programação dinâmica, grafos, matemática, etc.

Filosofia Pedagógica: Abordagem de Scaffolding (andaime). O agente nunca entrega o código final ou a resposta direta imediatamente. Ele guia o aluno através de dicas progressivas conceituais e de lógica.

Modo Solucionador: O agente possui um "botão de emergência" (ex: um comando de desistência explícito) onde altera seu estado para fornecer a resolução completa caso o aluno trave totalmente.

2. Interação e Interface (I/O)

Plataforma: Discord.

Gatilho de Ação: O agente operará de forma determinística via Slash Commands (ex: /teoria, /debug, /dica).

Isolamento de Sessão: A interação ocorrerá estritamente dentro de Threads específicas criadas para cada dúvida, isolando o contexto e a memória da conversa por aluno/problema.

Entradas Suportadas: Texto natural, links de juízes online (URI/Beecrowd, Codeforces) e blocos de código-fonte (snippets curtos).

3. Fontes de Dados e Ferramentas

Buscador Web / Scraper: Ferramenta ativa para buscar o problema online e, obrigatoriamente, recuperar o Editorial (Ground Truth) correspondente antes de iniciar a tutoria.

Base de Conhecimento: Ingestão de literatura clássica de maratona (ex: Competitive Programming do Halim) para embasamento de explicações teóricas.

Análise de Código: Feita exclusivamente via análise estática do LLM comparada ao editorial (sem execução em terminal/sandbox).

4. Restrições e Métricas

Infraestrutura: APIs comerciais de baixo custo focadas em código (OpenAI gpt-4o-mini ou DeepSeek V3/Coder).

Performance (SLA): Tempo de resposta das interações abaixo de 10 segundos (teto rígido de 15 segundos).

Avaliação de Qualidade: Validação contra um Golden Dataset de problemas e logs de conversas, feedback direto dos alunos, medição da Taxa de Resolução Autônoma e Custo por Sessão.

---

## 🛠️ Tech Stack

- **Orquestração de IA:** Python, CrewAI, LangChain, Anthropic Claude Code / OpenAI GPT-4.
- **Armazenamento Vetorial (RAG):** ChromaDB / Qdrant.
- **Integração & Interface:** Discord.py API.

---

## 📦 Configuração e Instalação

### Pré-requisitos
- Python 3.11 ou superior.
- Uma conta no Discord com um Bot Application configurado (Token).
- Chave de API da Anthropic ou OpenAI.

### 1. Clonar o repositório
```bash
git clone https://github.com/guijara/icpc-ai-tutor.git
cd icpc-ai-tutor
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_BOT_TOKEN=seu_token_do_discord
OPENAI_API_KEY=sua_chave_openai
ANTHROPIC_API_KEY=sua_chave_anthropic
CHROMADB_PATH=./data/chromadb
```

### 5. Ingerir materiais na Base Vetorial (RAG)
```bash
python scripts/ingest_docs.py
```

### 6. Iniciar o Bot do Discord
```bash
python src/bot.py
```

---

## 🤝 Impacto Educacional

O projeto atua diretamente no projeto de extensão da Universidade Federal de Mato Grosso (UFMT), reduzindo gargalos de atendimento aos alunos iniciantes e criando um ambiente seguro para o aprendizado prático e autônomo de estruturas de dados avançadas.

---

## 👨‍💻 Autor

Desenvolvido por **Guilherme Jara**  
[LinkedIn](https://linkedin.com/in/guilhermejara) | [GitHub](https://github.com/guijara)
