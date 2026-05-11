# rag.py

from pypdf import PdfReader

from vector_memory import VectorMemory


class RAGSystem:

    def __init__(self):

        self.memory = VectorMemory()

    # LOAD PDF
    def load_pdf(self, pdf_path):

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

        self.save_chunks(text)

        print("PDF berhasil dimasukkan ke vector DB")

    # LOAD TXT
    def load_txt(self, txt_path):

        with open(txt_path, "r") as f:

            text = f.read()

        self.save_chunks(text)

        print("TXT berhasil dimasukkan ke vector DB")

    # SAVE CHUNKS
    def save_chunks(self, text):

        chunk_size = 500

        chunks = [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

        for i, chunk in enumerate(chunks):

            chunk = chunk.strip()

            if chunk:

                self.memory.save_memory(
                    chunk,
                    f"chunk_{i}"
                )

    # QUERY
    def query(self, question):

        results = self.memory.search_memory(
            question
        )

        return results