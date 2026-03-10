import sys
import logging
import asyncio
sys.path.append("..")

from config import LOG_FILE, LOG_DIR, SALES_CSV_PATH
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

import os
os.makedirs(LOG_DIR, exist_ok=True)

# -------------------------
# Logger Setup
# -------------------------
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
        self.max_retries = 2
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
    # Check if Coder Needed
    # -------------------------
    def needs_coder(self, query: str) -> bool:
        """
        Only trigger coder for data analysis tasks,
        not for architecture or planning queries.
        """
        code_keywords = [
            "analyze csv",
            "analyse csv",
            "run code",
            "execute code",
            "calculate",
            "compute",
            "csv analysis",
            "data analysis",
            "write code",
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in code_keywords)

    # -------------------------
    # Full Pipeline
    # -------------------------
    async def run(self, user_query: str) -> str:
        logger.info(f"New query received: {user_query}")
        print(f"\n{'='*50}")
        print(f"NEXUS AI Processing: {user_query}")
        print(f"{'='*50}")

        # Fetch memory context
        memory_context = self.get_memory_context(user_query)
        enriched_query = user_query
        if memory_context:
            enriched_query = f"{user_query}\n\nContext from memory:\n{memory_context}"

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
            combined_research = enriched_query

        # -------------------------
        # Step 3: Coder (only for data tasks)
        # -------------------------
        code_output = ""
        if self.needs_coder(user_query):
            try:
                print("\n[NEXUS] Step 3: Running Coder...")
                logger.info("Step 3: Coder started.")

                data = None
                try:
                    from tools.file_tool import read_csv
                    data = read_csv(SALES_CSV_PATH)
                except Exception:
                    pass

                coder_result = await run_coder(
                    task=user_query,
                    context=combined_research[:500],
                    data=data,
                )
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
            final_report = await run_reporter(user_query, validated_output)
            logger.info("Report generated successfully.")
        except Exception as e:
            logger.error(f"Reporter failed: {e}")
            final_report = validated_output

        # Update Memory
        await self.update_memory(user_query, final_report)

        logger.info("Pipeline completed successfully.")
        return final_report