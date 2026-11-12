# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

The repository is in the specification phase: only `README.md` exists (written in Portuguese). No source code, `requirements.txt`, tests, or tooling has been committed yet. The README documents Phases 1–3 (spec, architecture, frameworks); treat those sections as the source of truth for design decisions. Update this file with real build/test/lint commands once code lands.

The README's setup section references planned entry points that do not exist yet:
- `pip install -r requirements.txt`
- `python scripts/ingest_docs.py` — ingest reference material into the vector DB
- `python src/bot.py` — start the Discord bot
- `.env` keys: `DISCORD_BOT_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `CHROMADB_PATH` (default `./data/chromadb`)

## What the product is

A Discord tutoring bot for ICPC/SBC competitive programming students at UFMT. Students submit failing code (TLE / WA / RTE), problem links (Beecrowd/URI, Codeforces), or theory questions. The bot answers with **scaffolded, Socratic hints and never gives the solution directly**. The one exception is an explicit "give up" command that switches to a full-solution mode.

## Architecture (decided in README Phases 2–3)

**Sequential (horizontal) multi-agent pipeline in CrewAI, ReWoo-style (Plan → Act → Synthesize):**
1. **Pesquisador (Researcher):** scrapes the problem statement from the web and *must* fetch the official editorial, which serves as hidden ground truth before tutoring starts.
2. **Analista de Código (Code Analyst):** checks syntax and Big-O complexity of the student's code against the editorial. This is **static LLM analysis only; code is never executed** (no sandbox).
3. **Tutor (Communicator):** writes the scaffolded hint.
4. **Revisor (Reflection):** reviews the Tutor's output and blocks anything that breaks the pedagogical rules (spoilers, full code) before it goes to Discord.

**RAG (theory):** ChromaDB `PersistentClient` stored on local disk. Indexing is agentic: an LLM writes structured summaries of the source PDFs (e.g. Halim's *Competitive Programming*) before they are stored. At bot runtime, retrieval is plain semantic search only.

**Discord layer:** Pycord (picked over discord.py for native slash-command and thread support). Interaction goes through deterministic slash commands (`/teoria`, `/debug`, `/dica`). Each question gets its own thread, which isolates context per student and problem.

**State:** the bot process is **stateless**, with no conversation state held in RAM. Thread/conversation history lives in Supabase (PostgreSQL), which is the source of truth so the bot survives restarts.

**LLM routing:** LiteLLM in front of low-cost code models (DeepSeek V3/Coder preferred; gpt-4o-mini as an alternative).

## Constraints to respect when implementing

- Response latency target is under 10 s, with a hard ceiling of 15 s per interaction. Keep the agent chain and its LLM calls lean.
- Quality is evaluated against a golden dataset of problems and conversation logs, plus autonomous-resolution rate and cost per session. Design so these can be logged and measured.
- The README's "Tech Stack" badge section (Discord.py, LangChain, Qdrant, Claude/GPT-4) is older than the Phase 3 decisions. Where they conflict, follow Phase 3: **Pycord, CrewAI + LiteLLM, ChromaDB, Supabase, DeepSeek**.
