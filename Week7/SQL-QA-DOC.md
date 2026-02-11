# SQL-QA-DOC — Week 7 Day 4 (Text-to-SQL System)

## Overview

The goal of **Week 7 – Day 4** was to design and implement a **Text-to-SQL Question Answering (QA) system**.  
This system allows users to ask questions in **natural language** and receive **accurate answers directly from a structured database**, without manually writing SQL queries.

Unlike RAG-based text systems, this task focuses on **structured data querying** using SQL.

---

## Problem Statement

Users often want answers like:
- “What was the total revenue in 2023?”
- “Which product generated the highest revenue?”
- “Show revenue grouped by region”

However, the data exists in a **relational database**, not in free text.

The challenge is to:
1. Understand the database schema
2. Convert natural language → SQL
3. Execute SQL safely
4. Return factual results

---

## High-Level Architecture

```text
User Question (Natural Language)
        ↓
LLM (Text → SQL Generation)
        ↓
Generated SQL Query
        ↓
SQLite Database Execution
        ↓
Query Result (Answer)
