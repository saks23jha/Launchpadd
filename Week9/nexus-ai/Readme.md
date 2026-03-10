# NEXUS AI
## Autonomous Multi-Agent AI System — Week 9 Day 5

---

## What is NEXUS AI?

NEXUS AI is a fully autonomous multi-agent AI system that can solve complex tasks
by orchestrating 8 specialized agents. It plans, researches, codes, analyzes,
critiques, optimizes, validates, and reports — all automatically.

---

## Capabilities

- Multi-agent orchestration
- Multi-step planning
- Parallel research execution
- Python code generation and execution
- Self-reflection and self-improvement
- Memory across sessions (Session + Vector + Long-Term)
- Logs and tracing
- Failure recovery

---

## Prerequisites

```bash
pip install autogen-agentchat autogen-ext faiss-cpu sentence-transformers python-dotenv
```

---

## Setup

**1. Clone or navigate to the project:**
```bash
cd Week9
```

**2. Create `.env` file in Week9/ root:**
```
OPENAI_API_KEY=your_groq_api_key_here
```

**3. Make sure the folder structure exists:**
```bash
mkdir -p nexus-ai/logs
mkdir -p nexus-ai/agents
mkdir -p memory
mkdir -p data
```

**4. Make sure `data/sales.csv` exists for CSV analysis tasks.**

---

## Running NEXUS AI

```bash
cd nexus-ai
python main.py
```

---

## Example Queries

```
You: Plan a startup in AI for healthcare
You: Generate backend architecture for a scalable app
You: Analyze CSV and create a business strategy
You: Design a RAG pipeline for 50k documents
You: exit
```

---

## Project Structure

```
Week9/
├── .env                          ← Groq API key
├── main_day1.py                  ← Day 1 runner
├── main_day2.py                  ← Day 2 runner
├── main_day3.py                  ← Day 3 runner
├── main_day4.py                  ← Day 4 runner
│
├── agents/                       ← Day 1, 2, 3 agents
├── orchestrator/                 ← Day 2, 3 planners
├── tools/                        ← Day 3 tools
├── memory/                       ← Day 4 memory systems
├── data/                         ← CSV and SQLite data
│
└── nexus-ai/                     ← Day 5 NEXUS AI
    ├── main.py
    ├── config.py
    ├── orchestrator.py
    ├── agents/
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
```

---

## How It Works

```
1. You type a query
2. Orchestrator fetches memory context
3. Planner breaks query into steps
4. Researcher studies all steps in parallel
5. Coder runs Python analysis (if needed)
6. Analyst extracts key insights
7. Critic finds flaws
8. Optimizer improves the output
9. Validator approves the result
10. Reporter writes the final answer
11. Memory systems updated
12. Final report shown to you
```

---

## Logs

All agent activity is logged to `nexus-ai/logs/nexus.log`:
```
2024-01-01 10:00:00 [INFO] NEXUS AI Orchestrator initialized.
2024-01-01 10:00:01 [INFO] New query received: Plan a startup...
2024-01-01 10:00:02 [INFO] Step 1: Planner started.
...
```