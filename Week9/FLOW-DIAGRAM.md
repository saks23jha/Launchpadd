# Week 9 – Day 2: Planner–Executor Multi-Agent System

## Overview
This system demonstrates a hierarchical multi-agent architecture using a Planner–Executor model.  
Unlike Day 1, which focused on linear agent pipelines, Day 2 introduces task planning, delegation, reflection, and validation to simulate real-world autonomous AI coordination.

The goal is to show how a central planner can orchestrate multiple worker agents, refine results, and enforce quality through validation.

---

## High-Level Flow Diagram

User Query  
↓  
Planner / Orchestrator  
↓  
Task Graph Generation  
↓  
Worker Agent(s)  
↓  
Planner (Reflection Phase)  
↓  
Validator Agent  
↓  
Final Approved Answer  

---

## Step-by-Step Execution Flow

### 1. User Input
The system begins when the user provides a query via the command line.  
This query is passed directly to the Planner.

---

### 2. Planner / Orchestrator
The Planner acts as the control unit of the system.

Responsibilities:
- Understand the user query
- Break the query into multiple executable tasks (task graph)
- Delegate each task to a worker agent
- Collect all worker outputs
- Perform reflection to improve coherence
- Submit the refined output to the validator

The Planner does **not** execute tasks itself.

---

### 3. Task Graph Generation
The Planner converts the user query into a structured task list, for example:
- Research the topic
- Explain core concepts
- Provide a structured explanation

This represents DAG-based thinking, where tasks are independent and can be parallelized.

---

### 4. Worker Agents (Executors)
Worker agents are stateless executors.

Responsibilities:
- Execute exactly one assigned task
- Return task-specific output
- Avoid planning, validation, or reflection

Each task is handled by a fresh worker instance, enabling parallel execution by design.

---

### 5. Reflection Phase (Planner)
After collecting worker outputs, the Planner performs a reflection step.

Reflection includes:
- Removing obvious duplication
- Selecting the most complete explanation
- Improving coherence without summarizing or adding new facts

This phase improves output quality while preserving the execution-focused nature of Day 2.

---

### 6. Validator Agent
The Validator acts as a quality gate.

Responsibilities:
- Check correctness, completeness, and clarity
- Ensure the output addresses the user query
- Return a strict verdict:
  - APPROVED
  - or REJECTED with a reason

The Planner releases the final answer **only if approved**.

---

### 7. Final Answer
If the Validator approves, the refined output is presented to the user as the final answer.  
If rejected, execution fails with a validation error.

---

## Key Architectural Characteristics

- Planner–Executor hierarchy
- Explicit task graph generation
- Parallel-capable worker design
- Reflection without summarization
- Hard validation gate
- Clear execution trace

---

## Learning Outcome
This system demonstrates how autonomous AI systems can move beyond simple request-response patterns into structured planning, delegation, quality control, and orchestration — forming the foundation for advanced multi-agent workflows.