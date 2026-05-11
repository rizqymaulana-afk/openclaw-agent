# reflection.py

import ollama


class Reflection:

    def reflect(
        self,
        result
    ):

        messages = [
            {
                "role": "system",
                "content": """
Evaluasi hasil berikut.

Apakah hasil sudah bagus?

Berikan feedback singkat.
"""
            },
            {
                "role": "user",
                "content": result
            }
        ]

        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        return response[
            "message"
        ]["content"]