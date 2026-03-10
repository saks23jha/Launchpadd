import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

load_dotenv()


class MemoryAgentSystem:
    """
    Day 4 Memory Enabled Agent System
    """

    def __init__(self):

        # Memory Systems
        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()
        self.long_term_memory = LongTermMemory()

        # LLM Client
        self.model_client = OpenAIChatCompletionClient(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=0.3,
            model_info={
                "provider": "groq",
                "family": "llama",
                "context_length": 8192,
                "vision": False,
                "function_calling": False,
                "json_output": False,
                "structured_output": False,
            },
        )

    # -------------------------
    # LLM Memory Trigger
    # -------------------------
    async def should_store_in_long_term(self, user_query: str, answer: str) -> bool:
        """
        Ask LLM if this exchange is worth storing in long term memory.
        """
        prompt = f"""
        You are a memory manager.

        Read this conversation exchange:
        User: {user_query}
        Agent: {answer}

        Decide if this contains important facts, preferences, or knowledge worth remembering long term.

        Reply with ONLY one word: yes or no
        """

        try:
            response = await self.model_client.create(
                messages=[UserMessage(content=prompt, source="user")]
            )
            decision = response.content.strip().lower()
            return decision == "yes"

        except Exception as e:
            print(f"[MEMORY TRIGGER] Failed to decide: {e}")
            return False

    # -------------------------
    # Generate Response
    # -------------------------
    async def generate_response(self, user_query: str) -> str:

        # Store user query in session memory
        self.session_memory.add_message("User", user_query)

        # Vector Memory Search
        try:
            similar_context = self.vector_store.search(user_query)
            memory_context = "\n".join(similar_context) if similar_context else "None"
        except Exception as e:
            print(f"[VECTOR STORE] Search failed: {e}")
            memory_context = "None"

        # Session Context
        session_context = self.session_memory.get_context()

        # Long Term Memory
        try:
            past_facts = self.long_term_memory.retrieve_all()
            long_term_context = "\n".join(past_facts) if past_facts else "None"
        except Exception as e:
            print(f"[LONG TERM MEMORY] Retrieve failed: {e}")
            long_term_context = "None"

        # Prompt Construction
        prompt = f"""
You are an intelligent assistant with memory.

Previous conversation:
{session_context}

Relevant past memories:
{memory_context}

Stored knowledge:
{long_term_context}

User Question:
{user_query}

Provide a helpful answer.
"""

        # LLM Call
        try:
            response = await self.model_client.create(
                messages=[UserMessage(content=prompt, source="user")]
            )
            answer = response.content

        except Exception as e:
            print(f"[LLM] Failed to generate response: {e}")
            return "Sorry, I could not generate a response."

        # Update Session Memory
        self.session_memory.add_message("Agent", answer)

        # Update Vector Memory
        try:
            self.vector_store.add(user_query)
            self.vector_store.add(answer)
        except Exception as e:
            print(f"[VECTOR STORE] Failed to add: {e}")

        # LLM decides if worth storing in long term memory
        should_store = await self.should_store_in_long_term(user_query, answer)
        if should_store:
            self.long_term_memory.store(user_query, category="fact")
            print("[LONG TERM MEMORY] Stored this exchange as important.")

        return answer


# -------------------------
# Interactive CLI Chat
# -------------------------
async def main():
    system = MemoryAgentSystem()

    print("\n=== Week 9 | Day 4 Memory Agent System ===\n")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_query = input("User: ").strip()

            if not user_query:
                continue

            if user_query.lower() == "exit":
                print("Goodbye!")
                break

            response = await system.generate_response(user_query)

            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        except Exception as e:
            print(f"\n[ERROR] {e}\n")


if __name__ == "__main__":
    asyncio.run(main())