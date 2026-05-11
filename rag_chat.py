# rag_chat.py

import ollama

from rag import RAGSystem


rag = RAGSystem()

# load knowledge base
rag.load_txt(
    "knowledge.txt"
)

print("=== RAG CHATBOT ===")

while True:

    question = input("\nYou: ")

    if question == "exit":

        break

    # retrieve context
    context = rag.query(
        question
    )

    # debug retrieved context
    print("\nRETRIEVED CONTEXT:")
    print(context)

    messages = [
        {
            "role": "system",
            "content": f"""
Kamu adalah AI RAG Assistant.

Jawab HANYA berdasarkan context berikut.

Jika jawaban tidak ada di context:
katakan "Saya tidak menemukan informasi tersebut di dokumen."

Context:

{context}
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    answer = response[
        "message"
    ]["content"]

    print("\nAgent:", answer)