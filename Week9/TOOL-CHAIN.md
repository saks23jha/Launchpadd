# Week 9 – Day 3  
# Tool-Chain Multi-Tool Execution System

## Overview

Day 3 introduces real tool integration into the system.  
Instead of only reasoning, the system can now:

- Execute Python code  
- Run SQL queries  
- Read and analyze CSV files  
- Chain multiple tools together  

This creates a practical multi-tool execution architecture.

---

## Architecture

```
User Query
     ↓
Day3Orchestrator
     ↓
Query Detection
     ↓
Tool Execution
     ↓
Output
```

The orchestrator determines which tool to use based on the query type.

---

## Implemented Tools

### 1. FileAgent

Handles file operations:

- Read `.txt`
- Write `.txt`
- Read `.csv`
- Write `.csv`

Returns CSV data as structured dictionaries.  
Performs no reasoning — only file I/O.

---

### 2. CodeExecutor

Executes dynamic Python code.

- Uses `exec()`
- Captures stdout
- Returns result or error

Example:
```
x=10;y=20;print(x+y)
```
Output:
```
30
```

---

### 3. DBAgent

Executes SQL queries using SQLite.

- Connects to database
- Ensures `insights` table exists
- Executes SELECT / INSERT / UPDATE / DELETE
- Returns query results

Example:
```
SELECT * FROM insights;
```

---

## Orchestrator Routing Logic

The `Day3Orchestrator` detects query type:

- Python-like syntax → **CodeExecutor**
- SQL keywords (SELECT, INSERT, etc.) → **DBAgent**
- Contains `sales.csv` → Full tool-chain

---

## Required Tool-Chain Example

User:
```
Analyze sales.csv and generate top 5 insights
```

Execution Flow:

1. FileAgent reads `sales.csv`
2. CodeExecutor computes:
   - Total revenue
   - Highest selling product
   - Lowest selling product
   - Total quantity sold
   - Average price
3. DBAgent stores insights
4. Final insights displayed

This demonstrates multi-tool chaining in a single request.

---

## How to Run

Activate environment:
```
source venv/bin/activate
```

Run:
```
python main_day3.py
```

Enter:
- Python code
- SQL query
- CSV analysis command

---

## Deliverables Completed

- FileAgent implemented  
- CodeExecutor implemented  
- DBAgent implemented  
- Orchestrator implemented  
- Python execution supported  
- SQL execution supported  
- CSV analysis tool-chain demonstrated  

All Day 3 requirements completed.