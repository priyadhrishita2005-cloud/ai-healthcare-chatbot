from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="db",
    embedding_function=embedding
)

results = db.similarity_search(
    "How to book appointment?"
)

print(results[0].page_content)