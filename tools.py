# tools.py

from datetime import datetime
from ddgs import DDGS


def calculator(expression):

    try:

        result = eval(expression)

        return str(result)

    except Exception as e:

        return str(e)


def current_time():

    now = datetime.now()

    return now.strftime("%H:%M:%S")


def web_search(query):

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(
            query,
            max_results=5
        )

        for r in search_results:

            results.append({
                "title": r["title"],
                "body": r["body"]
            })

    return str(results)