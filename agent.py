# agent.py

import json
import ollama

from vector_memory import VectorMemory
from memory import Memory
from memory_extractor import MemoryExtractor
from orchestrator import Orchestrator
from tool_definitions import TOOLS


class OpenClawAgent:

    def __init__(self):

        self.vector_memory = VectorMemory()

        self.memory = Memory()

        self.orchestrator = Orchestrator()

        self.memory_extractor = MemoryExtractor()

    def run(self, user_input):

        # =========================
        # SAVE USER MESSAGE
        # =========================

        self.memory.add(
            "user",
            user_input
        )

        # =========================
        # EXTRACT IMPORTANT MEMORY
        # =========================

        memory_data = self.memory_extractor.extract(
            user_input
        )

        if memory_data:

            if memory_data["type"] == "fact":

                # save persistent memory
                self.memory.save_fact(
                    memory_data["key"],
                    memory_data["value"]
                )

                # save vector memory
                self.vector_memory.save_memory(
                    f"{memory_data['key']}: {memory_data['value']}",
                    memory_data["key"]
                )

                print(
                    "MEMORY SAVED:",
                    memory_data
                )

        # =========================
        # MANUAL MEMORY RETRIEVAL
        # =========================

        # name
        if "siapa nama saya" in user_input.lower():

            name = self.memory.get_fact(
                "name"
            )

            if name:

                return f"Nama kamu {name}"

            else:

                return "Aku belum tahu nama kamu."

        # favorite
        if "apa yang saya suka" in user_input.lower():

            favorite = self.memory.get_fact(
                "favorite"
            )

            if favorite:

                return f"Kamu suka {favorite}"

            else:

                return "Aku belum tahu preference kamu."

        # job
        if "apa pekerjaan saya" in user_input.lower():

            job = self.memory.get_fact(
                "job"
            )

            if job:

                return f"Pekerjaan kamu adalah {job}"

            else:

                return "Aku belum tahu pekerjaan kamu."

        # city
        if "saya tinggal dimana" in user_input.lower():

            city = self.memory.get_fact(
                "city"
            )

            if city:

                return f"Kamu tinggal di {city}"

            else:

                return "Aku belum tahu tempat tinggal kamu."

        # =========================
        # GET MEMORIES
        # =========================

        facts = self.memory.get_all_facts()

        relevant_memories = self.vector_memory.search_memory(
            user_input
        )

        # =========================
        # SYSTEM PROMPT
        # =========================

        system_prompt = f"""
Kamu adalah OpenClaw AI Agent.

Informasi tentang user:

{facts}

Relevant memories:

{relevant_memories}

Kamu memiliki tools berikut:

{json.dumps(TOOLS, indent=2)}

ATURAN:

1. Jika user meminta:
- perhitungan matematika
- waktu sekarang
- pencarian internet

Maka jawab HANYA JSON seperti ini:

{{
  "tool": "nama_tool",
  "arguments": {{
    "parameter": "value"
  }}
}}

2. Jika user hanya ngobrol biasa:
- jawab natural seperti ChatGPT
- JANGAN gunakan JSON
"""

        # =========================
        # BUILD MESSAGES
        # =========================

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(
            self.memory.get_history()
        )

        # =========================
        # FIRST LLM CALL
        # =========================

        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        assistant_reply = response[
            "message"
        ]["content"]

        # =========================
        # CLEAN JSON MARKDOWN
        # =========================

        assistant_reply = assistant_reply.replace(
            "```json",
            ""
        )

        assistant_reply = assistant_reply.replace(
            "```",
            ""
        )

        assistant_reply = assistant_reply.strip()

        # =========================
        # TRY TOOL CALLING
        # =========================

        try:

            # cari posisi JSON
            json_start = assistant_reply.find("{")

            json_end = assistant_reply.rfind("}") + 1

            json_text = assistant_reply[
            json_start:json_end
            ]

            tool_call = json.loads(
            json_text
            )

            tool_name = tool_call[
                "tool"
            ]

            arguments = tool_call[
                "arguments"
            ]

            tool_result = self.orchestrator.execute(
                tool_name,
                arguments
            )

            print("TOOL NAME:", tool_name)

            print("ARGUMENTS:", arguments)

            print("TOOL RESULT:", tool_result)

            # =========================
            # FINAL RESPONSE GENERATION
            # =========================

            final_messages = [
                {
                    "role": "system",
                    "content": """
Kamu adalah AI assistant.

JANGAN gunakan format JSON.

Jawab natural seperti ChatGPT.
"""
                },
                {
                    "role": "user",
                    "content": f"""
User request:
{user_input}

Tool Result:
{tool_result}
"""
                }
            ]

            print(
                "GENERATING FINAL RESPONSE..."
            )

            final_response = ollama.chat(
                model="llama3",
                messages=final_messages
            )

            answer = final_response[
                "message"
            ]["content"]

            # fallback guardrail
            if '"tool"' in answer:

                answer = f"""
Berikut hasil tool:

{tool_result}
"""

        except Exception as e:

            print("DEBUG ERROR:", e)

            answer = assistant_reply

        # =========================
        # SAVE ASSISTANT RESPONSE
        # =========================

        self.memory.add(
            "assistant",
            answer
        )

        return answer