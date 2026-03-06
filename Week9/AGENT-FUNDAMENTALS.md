# Week 9 – Day 1: Multi-Agent System Using AutoGen

## Objective
The objective of Week 9 – Day 1 is to design and implement a multi-agent AI system (not a chatbot) that demonstrates agent-based architecture, message-based communication, role isolation, the Perception → Reasoning → Action loop, controlled memory using a message window, and explicit orchestration of agents. The focus of this task is on system design and architectural understanding rather than UI development or tool integrations.

## System Architecture
The system follows a fixed, sequential pipeline:
User → Research Agent → Summarizer Agent → Answer Agent → User  
Each agent has a single, well-defined responsibility and communicates exclusively through message passing.

## Agents Overview
**Research Agent** performs detailed research on the user query and produces structured, factual information. It does not summarize, answer the user directly, or add opinions.  
**Summarizer Agent** condenses the research output into a concise internal summary. It does not perform research, add new information, or answer the user.  
**Answer Agent** generates the final user-facing response using only the summarized content. It does not perform research or reference internal agents or intermediate steps.

## Core Concepts Implemented
The system uses true AI agents rather than chatbots, with each agent operating under a fixed role defined by a system prompt. Communication is message-based using asynchronous calls (`on_messages`), with no shared global state and no direct function calls between agents. Every interaction follows the Perception → Reasoning → Action loop: the agent receives a message, processes it internally, and produces a response. Each agent enforces a memory window (`memory_window = 10`) to limit how many recent messages are used for reasoning, which helps control token usage and maintain focus. Role isolation ensures that each agent can only perform its assigned responsibility.

## Model and Provider Configuration
The system uses the `llama-3.1-8b-instant` model via Groq’s OpenAI-compatible API. AutoGen’s `OpenAIChatCompletionClient` is used with the base URL set to `https://api.groq.com/openai/v1`.

## Environment Setup
A Python virtual environment is created and activated. Required dependencies are installed using `pip install pyautogen python-dotenv "autogen-ext[openai]"`. The Groq API key is exported as `OPENAI_API_KEY` via the terminal and also stored in a `.env` file, which is added to `.gitignore`.

## Project Structure
The project consists of an `agents` directory containing `research_agent.py`, `summarizer_agent.py`, and `answer_agent.py`, along with `main.py`, `.env`, and `README.md` at the root.

## Running the Project
The system is executed using `python main.py`. During execution, a user query flows through the Research Agent, then the Summarizer Agent, and finally the Answer Agent, which produces the final response shown to the user.

## Day 1 Deliverables
This implementation satisfies all Day 1 requirements: a multi-agent architecture, message-based communication, strict role isolation, memory window enforcement, asynchronous orchestration, a working test conversation, and no UI or tool integrations.

## Learning Outcome
This task demonstrates how agent-based systems differ from traditional chatbots and shows how to design modular, controllable AI workflows using AutoGen.