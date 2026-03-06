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

    
        # LLM Client (Groq)
    
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

    
    # Generate Response
    
    async def generate_response(self, user_query):

        # Store user query in session memory
        self.session_memory.add_message("User", user_query)

    
        # Vector Memory Search
    
        similar_context = self.vector_store.search(user_query)
        memory_context = "\n".join(similar_context)

    
        # Session Context
    
        session_context = self.session_memory.get_context()

    
        # Long Term Memory
    
        past_facts = self.long_term_memory.retrieve_all()
        long_term_context = "\n".join(past_facts)

        
        # Prompt Construction
    
        prompt = f"""
You are an intelligent assistant.

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
        
        response = await self.model_client.create(
            messages=[UserMessage(content=prompt, source="user")]
        )

        answer = response.content

    
        # Update Session Memory

        self.session_memory.add_message("Agent", answer)

    
        # Update Vector Memory
    
        self.vector_store.add(user_query)
        self.vector_store.add(answer)

        
        # Store Important Knowledge
        
        if "important" in user_query.lower():
            self.long_term_memory.store(user_query)

        return answer



# Interactive CLI Chat


async def main():

    system = MemoryAgentSystem()

    print("\n=== Week 9 | Day 4 Memory Agent System ===\n")
    print("Type 'exit' to quit\n")

    while True:

        user_query = input("User: ")

        if user_query.lower() == "exit":
            break

        response = await system.generate_response(user_query)

        print("\nAgent:", response)
        print()


if __name__ == "__main__":
    asyncio.run(main())