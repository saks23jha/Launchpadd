import asyncio
from dotenv import load_dotenv

load_dotenv()

from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import UserProxyAgent

from agents.research_agent import create_research_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.answer_agent import create_answer_agent


research_agent = create_research_agent()
summarizer_agent = create_summarizer_agent()
answer_agent = create_answer_agent()

user = UserProxyAgent(name="user")


async def run_test_conversation(user_query: str):
    print("\nUSER QUERY:")
    print(user_query)

    # User → Research Agent
    research_response = await research_agent.on_messages(
        [TextMessage(content=user_query, source="user")],
        cancellation_token=None,
    )
    research_output = research_response.chat_message.content

    print("\nRESEARCH AGENT OUTPUT:")
    print(research_output)

    # Research → Summarizer Agent
    summary_response = await summarizer_agent.on_messages(
        [TextMessage(content=research_output, source="research_agent")],
        cancellation_token=None,
    )
    summary_output = summary_response.chat_message.content

    print("\nSUMMARIZER AGENT OUTPUT:")
    print(summary_output)

    # Summarizer → Answer Agent
    final_response = await answer_agent.on_messages(
        [TextMessage(content=summary_output, source="summarizer_agent")],
        cancellation_token=None,
    )
    final_answer = final_response.chat_message.content

    print("\nFINAL ANSWER (USER SEES THIS):")
    print(final_answer)


if __name__ == "__main__":
    user_query = input("\nEnter your question: ").strip()

    if not user_query:
        print("Please enter a valid question.")
    else:
        asyncio.run(run_test_conversation(user_query))