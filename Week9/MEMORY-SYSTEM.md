# MEMORY-SYSTEM.md
## Week 9 — Day 4: Memory Systems

---

## Overview

Day 4 focused on building a memory-enabled AI agent system that can remember context across conversations using three distinct memory layers: short-term session memory, long-term persistent memory, and vector-based similarity memory.

---

## Memory Architecture

```
User Query
    ↓
Search Vector Memory   ← find similar past context
Fetch Session Memory   ← get current conversation history
Fetch Long Term Memory ← get stored facts from SQLite
    ↓
Inject all context into prompt
    ↓
LLM generates response
    ↓
Update Session Memory  ← add to current conversation
Update Vector Memory   ← store query + response as embeddings
LLM decides → Store in Long Term Memory? (yes/no)
```

---

## Memory Systems

### 1. Short-Term Memory — `session_memory.py`

- Stores conversation history during runtime only
- Uses a sliding window of last N messages (default: 10)
- Lost when the program exits
- Used to maintain conversational context within a session

**Key methods:**
- `add_message(role, content)` — adds a message to the window
- `get_history()` — returns all stored messages
- `get_context()` — returns formatted conversation string
- `clear()` — wipes the session memory

---

### 2. Long-Term Memory — `long_term_memory.py`

- Persists important facts across sessions using SQLite
- Stored in `memory/long_term.db`
- Survives program restarts
- LLM decides what is worth storing (not a keyword trigger)



**Key methods:**
- `store(content, category)` — saves a fact to SQLite
- `retrieve_all()` — fetches all stored memories
- `retrieve_by_category(category)` — fetches memories by tag
- `clear()` — deletes all stored memories

---

### 3. Vector Memory — `vector_store.py`

- Converts text into embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores embeddings in a FAISS index
- Performs similarity search to find relevant past context
- Persists to disk across sessions

**Persistence files:**
- `memory/faiss.index` — stores the FAISS embeddings
- `memory/faiss_texts.txt` — stores the original text mapped to each embedding

**Key methods:**
- `add(text)` — encodes text and adds to FAISS index
- `search(query, k=3)` — finds k most similar past entries
- `_save()` — saves index and texts to disk
- `_load()` — loads existing index and texts from disk

---

## How All 3 Work Together — `main_day4.py`

```python
# 1. Search vector memory for similar past context
similar_context = self.vector_store.search(user_query)

# 2. Get current session history
session_context = self.session_memory.get_context()

# 3. Get stored long term facts
past_facts = self.long_term_memory.retrieve_all()

# 4. Inject all into prompt
prompt = f"""
Previous conversation: {session_context}
Relevant past memories: {memory_context}
Stored knowledge: {long_term_context}
User Question: {user_query}
"""

# 5. LLM generates response

# 6. Update all memory systems
self.session_memory.add_message("Agent", answer)
self.vector_store.add(user_query)
self.vector_store.add(answer)

# 7. LLM decides if worth storing long term
if should_store:
    self.long_term_memory.store(user_query, category="fact")
```

---

## LLM-Based Memory Trigger
 the LLM itself makes the decision:

```
Prompt to LLM:
"Does this exchange contain important facts worth remembering long term?"
LLM replies: yes / no
```

This makes memory storage smarter and context-aware.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Short-term memory | Python list (sliding window) |
| Long-term memory | SQLite |
| Vector memory | FAISS + sentence-transformers |
| Embedding model | all-MiniLM-L6-v2 (384 dimensions) |
| LLM | llama-3.1-8b-instant via Groq |

---

## File Structure

```
Week9/
├── memory/
│   ├── session_memory.py     ← short-term memory
│   ├── vector_store.py       ← FAISS vector memory
│   ├── long_term_memory.py   ← SQLite persistent memory
│   ├── long_term.db          ← SQLite database file
│   ├── faiss.index           ← FAISS index file
│   └── faiss_texts.txt       ← original texts mapped to embeddings
└── main_day4.py              ← memory agent runner
```

---

## Test Results

The system successfully demonstrated:
- Remembering name, age, and workplace across sessions
- Recalling Docker-related discussions via vector similarity search
- Summarising all known facts about the user from combined memory sources
- LLM correctly deciding which exchanges are worth storing long term