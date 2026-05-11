# planner.py

import ollama


class Planner:

    def create_plan(
        self,
        goal
    ):

        messages = [
            {
                "role": "system",
                "content": """
Kamu adalah AI planner.

Buat step-by-step plan
untuk menyelesaikan goal user.

Jawab dalam bentuk numbered list.
"""
            },
            {
                "role": "user",
                "content": goal
            }
        ]

        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        return response[
            "message"
        ]["content"]