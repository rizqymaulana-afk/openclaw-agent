# memory.py

import json


class Memory:

    def __init__(self):

        self.history = []

        self.memory_file = "data/memory.json"

        self.facts = self.load_memory()

    # load persistent memory
    def load_memory(self):

        try:

            with open(
                self.memory_file,
                "r"
            ) as f:

                return json.load(f)

        except:

            return {}

    # save persistent memory
    def save_memory(self):

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                self.facts,
                f,
                indent=4
            )

    # conversation history
    def add(self, role, content):

        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):

        return self.history

    # semantic memory
    def save_fact(
        self,
        key,
        value
    ):

        self.facts[key] = value

        self.save_memory()

    def get_fact(
        self,
        key
    ):

        return self.facts.get(key)

    def get_all_facts(self):

        return self.facts