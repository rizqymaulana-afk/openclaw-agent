# memory_manager.py

import json
import os


class MemoryManager:

    def __init__(self):

        self.memory_file = (
            "memory.json"
        )

    # =========================
    # SAVE MEMORY
    # =========================

    def save_memory(
        self,
        data
    ):

        with open(
            self.memory_file,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # =========================
    # LOAD MEMORY
    # =========================

    def load_memory(
        self
    ):

        if not os.path.exists(
            self.memory_file
        ):

            return None

        with open(
            self.memory_file,
            "r"
        ) as file:

            return json.load(file)