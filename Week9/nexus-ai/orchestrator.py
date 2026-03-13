import sys
import re
import os
import logging
import asyncio
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config import LOG_FILE, LOG_DIR, SALES_CSV_PATH, MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO
from agents.planner import run_planner
from agents.researcher import run_researcher
from agents.coder import run_coder
from agents.analyst import run_analyst
from agents.critic import run_critic
from agents.optimizer import run_optimizer
from agents.validator import run_validator
from agents.reporter import run_reporter

from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("nexus-ai")


class NexusOrchestrator:

    def __init__(self):
        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()
        self.long_term_memory = LongTermMemory()
        logger.info("NEXUS AI Orchestrator initialized.")

    # -------------------------
    # Memory Context
    # -------------------------
    def get_memory_context(self, query: str) -> str:
        try:
            similar = self.vector_store.search(query)
            past_facts = self.long_term_memory.retrieve_all()
            session = self.session_memory.get_context()

            context = ""
            if session:
                context += f"Previous conversation:\n{session}\n\n"
            if similar:
                context += f"Relevant past memories:\n{chr(10).join(similar)}\n\n"
            if past_facts:
                context += f"Stored knowledge:\n{chr(10).join(past_facts[:5])}\n\n"

            return context.strip()

        except Exception as e:
            logger.warning(f"Memory fetch failed: {e}")
            return ""

    # -------------------------
    # Update Memory
    # -------------------------
    async def update_memory(self, query: str, final_report: str):
        try:
            self.session_memory.add_message("User", query)
            self.session_memory.add_message("NEXUS", final_report[:300])
            self.vector_store.add(query)
            self.vector_store.add(final_report[:300])
            self.long_term_memory.store(
                f"Query: {query[:100]} | Report: {final_report[:200]}",
                category="nexus"
            )
            logger.info("Memory updated successfully.")
        except Exception as e:
            logger.warning(f"Memory update failed: {e}")

    # -------------------------
    # LLM decides if Coder needed
    # -------------------------
    async def needs_coder(self, query: str) -> bool:
        system_prompt = """
        You are a binary decision agent.
        Reply with ONLY the single word: yes or no
        No explanation. No punctuation. No markdown. Just one word.

        Think carefully about the user's intent:

        Reply yes if the user wants to:
        - Write, generate, create, or implement any code
        - Build or design any technical system, pipeline, or architecture
        - Perform data analysis or calculations
        - Execute or run any algorithm

        Reply no if the user wants to:
        - Plan a business or startup
        - Get an explanation or research on a topic
        - Understand concepts or theories
        - Get general advice or recommendations
        """

        model_client = OpenAIChatCompletionClient(
            model=MODEL_NAME,
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=0.0,
            model_info=MODEL_INFO,
        )

        router = AssistantAgent(
            name="code_router",
            system_message=system_prompt,
            model_client=model_client,
        )

        try:
            response = await router.on_messages(
                [TextMessage(content=query, source="orchestrator")],
                cancellation_token=None,
            )

            decision = response.chat_message.content.strip().lower().split()[0]
            decision = decision.replace("*", "").replace(".", "").replace(",", "")
            print(f"[CODE ROUTER] Decision: {decision}")
            return decision == "yes"

        except Exception as e:
            logger.warning(f"Code router failed: {e}")
            return False

    # -------------------------
    # LLM decides if CSV needed
    # -------------------------
    async def needs_csv(self, query: str) -> bool:
        system_prompt = """
        You are a binary decision agent.
        Reply with ONLY the single word: yes or no
        No explanation. No punctuation. No markdown. Just one word.

        Think carefully:

        Reply yes ONLY if the user specifically wants to:
        - Analyze existing sales, revenue, or product data
        - Process or query a CSV or database

        Reply no if the user wants to:
        - Write general code or algorithms
        - Build pipelines or architecture
        - Do math or general programming tasks
        """

        model_client = OpenAIChatCompletionClient(
            model=MODEL_NAME,
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=0.0,
            model_info=MODEL_INFO,
        )

        router = AssistantAgent(
            name="csv_router",
            system_message=system_prompt,
            model_client=model_client,
        )

        try:
            response = await router.on_messages(
                [TextMessage(content=query, source="orchestrator")],
                cancellation_token=None,
            )

            decision = response.chat_message.content.strip().lower().split()[0]
            decision = decision.replace("*", "").replace(".", "").replace(",", "")
            print(f"[CSV ROUTER] Decision: {decision}")
            return decision == "yes"

        except Exception as e:
            logger.warning(f"CSV router failed: {e}")
            return False

    # -------------------------
    # LLM decides if pipeline
    # -------------------------
    async def is_pipeline_query(self, query: str) -> bool:
        system_prompt = """
        You are a binary decision agent.
        Reply with ONLY the single word: yes or no
        No explanation. No punctuation. No markdown. Just one word.

        Reply yes if the user wants to:
        - Design, create, or build any kind of pipeline
        - Examples: RAG pipeline, ETL pipeline, data pipeline,
          NLP pipeline, training pipeline, chunking pipeline

        Reply no for everything else.
        """

        model_client = OpenAIChatCompletionClient(
            model=MODEL_NAME,
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=0.0,
            model_info=MODEL_INFO,
        )

        router = AssistantAgent(
            name="pipeline_router",
            system_message=system_prompt,
            model_client=model_client,
        )

        try:
            response = await router.on_messages(
                [TextMessage(content=query, source="orchestrator")],
                cancellation_token=None,
            )

            decision = response.chat_message.content.strip().lower().split()[0]
            decision = decision.replace("*", "").replace(".", "").replace(",", "")
            print(f"[PIPELINE ROUTER] Decision: {decision}")
            return decision == "yes"

        except Exception as e:
            logger.warning(f"Pipeline router failed: {e}")
            return False

    # -------------------------
    # LLM generates filename
    # -------------------------
    async def get_pipeline_filename(self, query: str) -> str:
        system_prompt = """
        You are a filename generator agent.
        Given a user query about a pipeline, generate a clean Python filename.

        Rules:
        - Use snake_case
        - End with _pipeline
        - No spaces, no special characters, no extension
        - Maximum 30 characters
        - Examples:
          "design a RAG pipeline" → rag_pipeline
          "create chunking pipeline" → chunking_pipeline
          "build ETL pipeline for sales" → etl_pipeline
          "NLP text classification pipeline" → nlp_pipeline

        Reply with ONLY the filename, nothing else.
        """

        model_client = OpenAIChatCompletionClient(
            model=MODEL_NAME,
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=0.0,
            model_info=MODEL_INFO,
        )

        agent = AssistantAgent(
            name="filename_agent",
            system_message=system_prompt,
            model_client=model_client,
        )

        try:
            response = await agent.on_messages(
                [TextMessage(content=query, source="orchestrator")],
                cancellation_token=None,
            )

            filename = response.chat_message.content.strip().lower()
            filename = re.sub(r'[^a-z0-9_]', '', filename)[:30]
            print(f"[FILENAME AGENT] Pipeline filename: {filename}")
            return filename or "pipeline"

        except Exception as e:
            logger.warning(f"Filename agent failed: {e}")
            return "pipeline"

    # -------------------------
    # Generate MD Filename from query
    # -------------------------
    def get_md_filename(self, query: str) -> str:
        clean = query.lower().strip()
        clean = re.sub(r'[^a-z0-9\s]', '', clean)
        clean = clean.strip().replace(" ", "_")[:40]
        return f"{clean}.md"

    # -------------------------
    # Save Pipeline Files
    # -------------------------
    def save_pipeline_files(self, filename_base: str, code: str, md_report: str):
        py_path = os.path.join(os.getcwd(), f"{filename_base}.py")
        md_path = os.path.join(os.getcwd(), f"{filename_base}.md")

        try:
            with open(py_path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"\n[NEXUS] Pipeline code saved to {py_path} ✅")
            logger.info(f"Pipeline code saved to {py_path}")
        except Exception as e:
            print(f"\n[NEXUS] Failed to save .py file: {e}")
            logger.error(f"Pipeline .py save failed: {e}")

        try:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_report)
            print(f"[NEXUS] Pipeline explanation saved to {md_path} ✅")
            logger.info(f"Pipeline explanation saved to {md_path}")
        except Exception as e:
            print(f"\n[NEXUS] Failed to save .md file: {e}")
            logger.error(f"Pipeline .md save failed: {e}")

    # -------------------------
    # Save MD Report
    # -------------------------
    def save_md_report(self, query: str, report: str):
        filename = self.get_md_filename(query)
        filepath = os.path.join(os.getcwd(), filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n[NEXUS] Report saved to {filepath} ✅")
            logger.info(f"MD report saved to {filepath}")
        except Exception as e:
            print(f"\n[NEXUS] Failed to save .md report: {e}")
            logger.error(f"MD report save failed: {e}")

    # -------------------------
    # Full Pipeline
    # -------------------------
    async def run(self, user_query: str) -> str:
        logger.info(f"New query received: {user_query}")
        print(f"\n{'='*50}")
        print(f"NEXUS AI Processing: {user_query}")
        print(f"{'='*50}")

        # All routing decisions made by LLM
        is_pipeline = await self.is_pipeline_query(user_query)
        pipeline_filename = ""
        if is_pipeline:
            pipeline_filename = await self.get_pipeline_filename(user_query)
            print(f"\n[NEXUS] Pipeline detected! Will save as {pipeline_filename}.py and {pipeline_filename}.md")

        # Fetch memory context — background only
        memory_context = self.get_memory_context(user_query)
        enriched_query = user_query
        if memory_context:
            enriched_query = f"""
Current query: {user_query}

For background context only (do NOT apply previous query details to current query):
{memory_context}
"""

        # -------------------------
        # Step 1: Planner
        # -------------------------
        try:
            print("\n[NEXUS] Step 1: Planning...")
            logger.info("Step 1: Planner started.")
            steps = await run_planner(enriched_query)
            logger.info(f"Planner generated {len(steps)} steps.")
        except Exception as e:
            logger.error(f"Planner failed: {e}")
            return "NEXUS AI failed at planning stage. Please try again."

        # -------------------------
        # Step 2: Researcher (parallel)
        # -------------------------
        try:
            print("\n[NEXUS] Step 2: Researching all steps in parallel...")
            logger.info("Step 2: Researcher started.")
            research_tasks = [run_researcher(step) for step in steps]
            research_results = await asyncio.gather(*research_tasks)
            combined_research = "\n\n".join(research_results)
            logger.info("Research completed.")
        except Exception as e:
            logger.error(f"Researcher failed: {e}")
            combined_research = user_query

        # -------------------------
        # Step 3: Coder (LLM decides)
        # -------------------------
        code_output = ""
        generated_code = ""
        coder_needed = await self.needs_coder(user_query)

        if coder_needed:
            try:
                print("\n[NEXUS] Step 3: Running Coder...")
                logger.info("Step 3: Coder started.")

                data = None
                if not is_pipeline:
                    csv_needed = await self.needs_csv(user_query)
                    if csv_needed:
                        try:
                            from tools.file_tool import read_csv
                            data = read_csv(SALES_CSV_PATH)
                            print("[NEXUS] CSV data loaded for analysis.")
                        except Exception:
                            pass
                    else:
                        print("[NEXUS] No CSV needed for this task.")

                coder_result = await run_coder(
                    task=user_query,
                    context=combined_research[:500],
                    data=data,
                )

                generated_code = coder_result["code"]

                if coder_result["success"]:
                    code_output = coder_result["output"]
                    logger.info("Coder completed successfully.")
                else:
                    logger.warning(f"Coder failed: {coder_result['error']}")

            except Exception as e:
                logger.error(f"Coder error: {e}")
        else:
            print("\n[NEXUS] Step 3: Coder not needed, skipping.")

        # -------------------------
        # Step 4: Analyst
        # -------------------------
        try:
            print("\n[NEXUS] Step 4: Analyzing...")
            logger.info("Step 4: Analyst started.")
            analysis = await run_analyst(combined_research, code_output)
            logger.info("Analysis completed.")
        except Exception as e:
            logger.error(f"Analyst failed: {e}")
            analysis = combined_research

        # -------------------------
        # Step 5: Critic + Optimizer
        # -------------------------
        optimized = analysis
        try:
            print(f"\n[NEXUS] Step 5: Critic reviewing...")
            logger.info("Step 5: Critic started.")
            critique = await run_critic(optimized)

            if "NO FLAWS FOUND" in critique.upper():
                print("\n[NEXUS] Critic found no flaws. Skipping optimizer.")
                logger.info("Critic found no flaws.")
            else:
                print(f"\n[NEXUS] Step 6: Optimizing based on critique...")
                logger.info("Step 6: Optimizer started.")
                optimized = await run_optimizer(optimized, critique)
                logger.info("Optimization completed.")

        except Exception as e:
            logger.error(f"Critic/Optimizer failed: {e}")

        # -------------------------
        # Step 7: Validator
        # -------------------------
        validated_output = optimized
        try:
            print(f"\n[NEXUS] Step 7: Validating...")
            logger.info("Step 7: Validator started.")
            result = await run_validator(optimized)

            if result["approved"]:
                validated_output = optimized
                logger.info("Validator approved the output.")
            else:
                logger.warning(f"Validator rejected: {result['verdict']}")
                print("\n[NEXUS] Validator rejected. Using best available output.")
                validated_output = optimized

        except Exception as e:
            logger.error(f"Validator failed: {e}")
            validated_output = optimized

        # -------------------------
        # Step 8: Reporter
        # -------------------------
        try:
            print("\n[NEXUS] Step 8: Generating final report...")
            logger.info("Step 8: Reporter started.")

            enriched_output = validated_output
            if code_output:
                enriched_output = f"""
Generated Code:
{generated_code}

Execution Output:
{code_output}

Additional Context:
{validated_output[:1000]}
"""

            final_report = await run_reporter(
                user_query,
                enriched_output,
                is_pipeline=is_pipeline,
            )
            logger.info("Report generated successfully.")

        except Exception as e:
            logger.error(f"Reporter failed: {e}")
            final_report = validated_output

        # -------------------------
        # Save Pipeline Files (.py + .md)
        # -------------------------
        if is_pipeline and generated_code:
            self.save_pipeline_files(
                filename_base=pipeline_filename,
                code=generated_code,
                md_report=final_report,
            )

        # -------------------------
        # Auto save every query as .md
        # -------------------------
        else:
            self.save_md_report(user_query, final_report)

        # Update Memory
        await self.update_memory(user_query, final_report)

        logger.info("Pipeline completed successfully.")
        return final_report