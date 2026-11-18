# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Specification phase: there is no source code, `pyproject.toml`, tests or CI yet. `README.md` (Portuguese, private repo) is the source of truth for product and architecture decisions; `docs/decisoes.md` logs each decision with its alternatives and reasons. `docs/conceitos.md` is the learning map. `docs/plano-do-projeto.md` is a local-only planning document (gitignored). Work happens on the `develop` branch; `main` is not touched until the user says so. Spec changes go through OpenSpec (`openspec/`, `/openspec-propose`). Update this file with real build, lint and test commands once code lands.

Planned tooling (not installed yet): `uv` (env and deps), `ruff` (lint/format), `pytest` (evals that call an LLM get a separate marker and run only on demand), `pydantic-settings` for `.env`, layout `src/icpc_tutor/{bot,agents,tools,rag,db}`, `evals/`, `scripts/`.

## Working agreement with the user

- The user is learning how to build agents. For each piece you implement, briefly explain what it is and why it exists, and keep `docs/conceitos.md` (`[ENTENDER]` vs `[DELEGAR]`) and `docs/decisoes.md` up to date. Do not belabor tooling details like ruff, uv or CI config.
- Talk to the user in Portuguese (Brazil). Do not implement until the user asks.

## Product rules (non-negotiable)

Discord tutor for ICPC/SBC students at UFMT. The bot **never gives accepted code**; there is no "give up" command. At the end of the hint ladder it may explain the solution in natural language, and a short pseudocode only if the student asks for something more concrete. Hints are always in Portuguese; students send C++ or Python (Java is unsupported).

- Commands: only `/problema <link>` (opens a thread) and `/dica` (forces one level up). The bot answers every message inside the thread. Buttons "ajudou" / "não entendi" on replies; "não entendi" makes the Tutor simplify or use a metaphor without raising the level.
- Hint ladder: 1 understand the problem (questions only), 2 indirect direction (no technique name), 3 name the technique and *why* it applies (recognition signals), 4 apply it in prose. The Tutor decides when to advance (exit goal met, or two answers without progress); never skip levels.
- No scraping. Codeforces metadata comes from the public API `problemset.problems` (cached); for LeetCode/AtCoder/Beecrowd the student pastes the statement. The editorial is no longer required; weak ground truth = tags + rating + statement.

## Architecture

CrewAI sequential pipeline behind LiteLLM, ReWOO-style, with static analysis only (code is never executed):

1. **Router:** natural language vs. code.
2. **Pesquisador:** a plain tool, not an LLM agent (regex on the link + Codeforces cache).
3. **Problem analysis:** shared across students, cached and versioned in Supabase. Stores accepted techniques, recognition cues, a ready hint ladder, a confidence level and an own summary, **not the full statement**. Low confidence (no tags) makes the Tutor assert less.
4. **Code analysis:** per submission, only when code was sent.
5. **Tutor** then **Revisor** (deterministic rule check first, LLM that improves the answer second).

LLM calls per interaction: 3 with new code, 2 on a continuation, +1 the first time a problem appears. Models via AWS Bedrock (global inference profile, `us-east-1`): Claude Haiku 5.5 for router, Tutor, code analysis and Revisor; Claude Sonnet 5.5 for problem analysis; Titan Text Embeddings V2 for RAG. Run CrewAI outside the bot's event loop and `defer()` every slash command.

**State:** the bot is stateless. Supabase (PostgreSQL) holds `problems`, `problem_analyses`, `threads`, `messages`, `code_analyses`, `feedback`, `students` (Discord ID stored only as HMAC), with a per-thread lock against duplicate events. Messages and code are deleted after 30 days.

**RAG:** ChromaDB `PersistentClient`. Indexing is agentic (an LLM writes fixed-field summaries of each section). Sources: Halim 1 and 2 and cp-algorithms (from its GitHub repo, not scraped). Corpus and queries in English, with a Portuguese-name field. PDFs and the index live in `data/`, outside Git.

**Infra:** EC2 t4g.small (ARM) with an IAM role for 3 months of AWS credit, then Oracle Cloud Free (ARM). Dev (laptop, own bot token and Supabase project) is separate from prod (EC2). CI/CD from the start with GitHub Actions: CI on every PR; CD on merge to `main` via OIDC + Systems Manager, forward-only Supabase migrations, smoke test, rollback to the previous commit.

## Constraints

- SLA: p95 ≤ 20 s for the first hint, hard ceiling 30 s; reply "analisando..." immediately and edit.
- Treat everything from the student (code, statement, messages) as untrusted input (prompt injection); the Revisor is the last barrier. Do not hand agents tools with side effects.
- Never commit `.env`, tokens, the book PDFs or the vector index.
- Quality is measured with a golden dataset, deterministic rules plus an LLM judge (Sonnet 5.5), a single-call baseline, latency, cost per session and autonomous-resolution rate.

## Human vs. agent tasks

- Tasks marked `[HUMAN]` in `tasks.md` are actions only the user can perform
  (creating accounts, generating tokens, configuring cloud resources, approving spend).
  Never attempt them yourself.
- When you reach a `[HUMAN]` task, stop, list exactly what the user must do,
  and wait for confirmation before continuing.
- Before depending on a human task, verify its result when possible
  (e.g., check that an environment variable exists or that a connection test passes).
  If the check fails, stop and report what is missing. Do not invent values.
- Never create, guess, or hardcode credentials, tokens, account IDs, or other secrets.
- Tasks marked `[AGENT]` are yours to implement. Follow the requirements and
  scenarios in the active change's spec, and report any scenario that has no test.
- If a `[AGENT]` task depends on a `[HUMAN]` task, state the dependency
  (e.g., `blocked by: 1.2`) and do not proceed past it.
- For infrastructure changes, prepare the plan or configuration as a file for
  the user to review. Do not apply changes to cloud accounts without explicit approval.
