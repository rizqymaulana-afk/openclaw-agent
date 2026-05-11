# orchestrator.py

from tools import (
    calculator,
    current_time,
    web_search
)


class Orchestrator:

    def execute(
        self,
        tool_name,
        arguments
    ):

        if tool_name == "calculator":

            expression = arguments.get(
                "expression"
            )

            return calculator(expression)

        elif tool_name == "current_time":

            return current_time()

        elif tool_name == "web_search":

            query = arguments.get(
                "query"
            )

            return web_search(query)

        else:

            return "Tool tidak ditemukan"