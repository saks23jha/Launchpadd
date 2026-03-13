import asyncio
from typing import List, Dict

from autogen_agentchat.messages import TextMessage

from agents.worker_agent import create_worker_agent
from agents.validator import create_validator_agent


class Planner:
    """
    Planner / Orchestrator Agent

    Responsibilities:
    - Receive user query
    - Generate task graph
    - Delegate tasks to worker agents
    - Perform reflection on combined output
    - Send result to validator
    """

    def __init__(self):
        self.validator = create_validator_agent()

    # -----------------------------
    # Step 1: Task Graph Generation
    # -----------------------------
    def create_task_graph(self, user_query: str) -> List[Dict]:
        """
        Break the user query into executable tasks.
        This represents DAG-based task generation.
        """

        tasks = [
            {
                "task_id": 1,
                "description": f"Research the topic: {user_query}",
            },
            {
                "task_id": 2,
                "description": f"Explain the core concepts related to: {user_query}",
            },
            {
                "task_id": 3,
                "description": f"Provide a concise structured explanation for: {user_query}",
            },
        ]

        print("\n[PLANNER] Generated Task Graph:")
        for task in tasks:
            print(f"  - Task {task['task_id']}: {task['description']}")

        return tasks

    # -----------------------------
    # Step 2: Execute Tasks (PARALLEL)
    # -----------------------------
    async def execute_tasks(self, tasks: List[Dict]) -> List[str]:
        """
        Dispatch tasks to worker agents in parallel.
        """

        print("\n[PLANNER] Dispatching Tasks to Workers (Parallel Execution)")

        worker_jobs = []

        for task in tasks:
            worker = create_worker_agent()

            print(f"[PLANNER] Assigning Task {task['task_id']}")

            job = worker.on_messages(
                [TextMessage(content=task["description"], source="planner")],
                cancellation_token=None,
            )

            worker_jobs.append(job)

        # Run all workers simultaneously
        responses = await asyncio.gather(*worker_jobs)

        results = []

        for i, response in enumerate(responses):
            output = response.chat_message.content

            print(f"\n[WORKER OUTPUT - Task {tasks[i]['task_id']}]:")
            print(output)

            results.append(output)

        return results

    # -----------------------------
    # Step 3: Reflection
    # -----------------------------
    def reflect_on_results(self, worker_outputs: List[str]) -> str:
        """
        Reflection phase:
        - Remove obvious duplication
        - Keep the most complete explanation
        - Improve coherence without summarizing
        """

        print("\n[PLANNER] Performing Reflection Step")

        cleaned_outputs = [out.strip() for out in worker_outputs if out.strip()]
        cleaned_outputs.sort(key=len, reverse=True)

        refined_core = cleaned_outputs[0]

        refined_output = (
            "Refined Answer:\n"
            "----------------\n"
            f"{refined_core}"
        )

        return refined_output

    # -----------------------------
    # Step 4: Validation
    # -----------------------------
    async def validate_output(self, refined_output: str) -> str:
        """
        Send the refined output to the validator agent.
        """

        print("\n[PLANNER] Sending output to Validator")

        validation_response = await self.validator.on_messages(
            [TextMessage(content=refined_output, source="planner")],
            cancellation_token=None,
        )

        verdict = validation_response.chat_message.content

        print("\n[VALIDATOR VERDICT]:")
        print(verdict)

        if verdict.strip().upper().startswith("APPROVED"):
            return refined_output

        raise ValueError("Validation failed. Output rejected.")

    # -----------------------------
    # Full Orchestration
    # -----------------------------
    async def run(self, user_query: str) -> str:
        """
        Full Day-2 orchestration flow.
        """

        print("\n[PLANNER] Received User Query:")
        print(user_query)

        tasks = self.create_task_graph(user_query)

        worker_outputs = await self.execute_tasks(tasks)

        refined_output = self.reflect_on_results(worker_outputs)

        final_answer = await self.validate_output(refined_output)

        return final_answer