# test_rag.py

from rag import RAGSystem


rag = RAGSystem()

# load pdf
rag.load_pdf(
    "SKB 3 Menteri Libur Nasional dan Cuti Bersama Tahun 2026.pdf"
)

# query
result = rag.query(
    "berapa hari cuti?"
)

print(result)