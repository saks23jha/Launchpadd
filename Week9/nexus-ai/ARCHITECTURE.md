# ARCHITECTURE.md
## NEXUS AI — Autonomous Multi-Agent System Architecture

---

## Overview

NEXUS AI is a fully autonomous multi-agent AI system built on AutoGen and Groq.
It takes a user query and processes it through a pipeline of 9 specialized agents,
each with a distinct role, producing a clean professional report as output.

---

## System Architecture

```
User Query
    ↓
NexusOrchestrator
    ↓
┌─────────────────────────────────────────────┐
│  Step 1: Planner                            │
│  Breaks query into actionable steps         │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 2: Researcher (Parallel)              │
│  Researches all steps simultaneously        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 3: Coder (Conditional)                │
│  Runs only for data/CSV analysis tasks      │
│  Uses Day 3 code_executor tool              │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 4: Analyst                            │
│  Extracts insights from research + code     │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 5: Critic                             │
│  Identifies flaws in the analysis           │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 6: Optimizer                          │
│  Improves analysis based on critique        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 7: Validator                          │
│  Approves or rejects the optimized output   │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Step 8: Reporter                           │
│  Writes final clean user-facing report      │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  Memory Update                              │
│  Session + Vector + Long-Term Memory        │
└─────────────────────────────────────────────┘
    ↓
Final Report shown to User
```

---

## Agent Registry

| Agent | Role | Temperature |
|-------|------|-------------|
| Planner | Breaks query into steps | 0.2 |
| Researcher | Produces detailed research notes | 0.2 |
| Coder | Writes and executes Python code | 0.2 |
| Analyst | Extracts insights and conclusions | 0.2 |
| Critic | Identifies flaws and weaknesses | 0.3 |
| Optimizer | Improves output based on critique | 0.3 |
| Validator | Approves or rejects output | 0.0 |
| Reporter | Writes final user-facing report | 0.2 |

---

## Memory Architecture

```
┌─────────────────────────────────────────────┐
│  Session Memory (session_memory.py)         │
│  - Sliding window of last 10 messages       │
│  - Lost on program exit                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Vector Memory (vector_store.py)            │
│  - FAISS index with sentence embeddings     │
│  - Similarity search for past context       │
│  - Persists to disk (faiss.index)           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Long Term Memory (long_term_memory.py)     │
│  - SQLite database                          │
│  - LLM decides what to store               │
│  - Persists across sessions                 │
└─────────────────────────────────────────────┘
```

---

## Tool Integration (from Day 3)

| Tool | File | Used By |
|------|------|---------|
| Code Executor | tools/code_executor.py | Coder Agent |
| File Tool | tools/file_tool.py | Coder Agent |
| DB Tool | tools/db_tool.py | Available |

---

## Key Design Decisions

**Parallel Research:**
All planning steps are researched simultaneously using `asyncio.gather()`,
reducing total research time significantly.

**Conditional Coder:**
The Coder agent only runs when the query explicitly involves data analysis,
CSV processing, or code execution — not for planning or architecture queries.

**Self-Reflection Loop:**
Critic → Optimizer implements self-reflection and self-improvement.
The system critiques its own output and improves it before validation.

**Failure Recovery:**
Every pipeline step is wrapped in try/except. If any agent fails,
the system uses the best available output and continues to the next step.

**Memory Injection:**
Before planning, the orchestrator fetches relevant context from all 3 memory
systems and injects it into the query, making NEXUS AI context-aware across sessions.

---

## File Structure

```
nexus-ai/
├── main.py                  ← entry point, chat loop
├── config.py                ← all settings
├── orchestrator.py          ← master pipeline controller
├── agents/
│   ├── __init__.py
│   ├── planner.py
│   ├── researcher.py
│   ├── coder.py
│   ├── analyst.py
│   ├── critic.py
│   ├── optimizer.py
│   ├── validator.py
│   └── reporter.py
└── logs/
    └── nexus.log

Shared from previous days:
├── tools/
│   ├── code_executor.py     ← Day 3
│   ├── file_tool.py         ← Day 3
│   └── db_tool.py           ← Day 3
└── memory/
    ├── session_memory.py    ← Day 4
    ├── vector_store.py      ← Day 4
    └── long_term_memory.py  ← Day 4
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | AutoGen (Microsoft) |
| LLM | llama-3.1-8b-instant via Groq |
| Vector Memory | FAISS + sentence-transformers |
| Long Term Memory | SQLite |
| Code Execution | Python exec() |
| Logging | Python logging module |
| Environment | Python 3.12 + venv |