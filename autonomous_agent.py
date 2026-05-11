# autonomous_agent.py

import ollama

from planner import Planner
from reflection import Reflection

from tools import web_search


class AutonomousAgent:

    def __init__(self):

        self.planner = Planner()

        self.reflection = Reflection()

    def run(self, goal):

        # =========================
        # CREATE PLAN
        # =========================

        print("\nMEMBUAT PLAN...\n")

        plan = self.planner.create_plan(
            goal
        )

        print(plan)

        # =========================
        # CREATE SEARCH QUERY
        # =========================

        print("\nMEMBUAT SEARCH QUERY...\n")

        query_messages = [
            {
                "role": "system",
                "content": """
Buat search query Google yang optimal
berdasarkan goal user.

Jawab hanya query singkat.
"""
            },
            {
                "role": "user",
                "content": goal
            }
        ]

        query_response = ollama.chat(
            model="llama3",
            messages=query_messages
        )

        optimized_query = query_response[
            "message"
        ]["content"]

        print(
            "SEARCH QUERY:",
            optimized_query
        )

        # =========================
        # EXECUTE WEB SEARCH
        # =========================

        print("\nMENJALANKAN WEB SEARCH...\n")

        search_result = web_search(
            optimized_query
        )

        print(search_result)

        # =========================
        # GENERATE SUMMARY
        # =========================

        print("\nMEMBUAT SUMMARY...\n")

        summary_messages = [
            {
                "role": "system",
                "content": """
Kamu adalah AI Research Assistant.

Buat summary profesional
berdasarkan hasil research.

Format:
1. Ringkasan
2. Poin penting
3. Kesimpulan
"""
            },
            {
                "role": "user",
                "content": f"""
Goal:
{goal}

Search Result:
{search_result}
"""
            }
        ]

        summary_response = ollama.chat(
            model="llama3",
            messages=summary_messages
        )

        summary = summary_response[
            "message"
        ]["content"]

        print(summary)

        # =========================
        # SELF REFLECTION
        # =========================

        print("\nSELF REFLECTION...\n")

        feedback = self.reflection.reflect(
            summary
        )

        print(feedback)

        # =========================
        # FINAL RESULT
        # =========================

        return summary