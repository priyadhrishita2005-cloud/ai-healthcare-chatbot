from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

from transformers import pipeline

# Embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector DB
db = Chroma(
    persist_directory="db",
    embedding_function=embedding
)

# Free local AI model
pipe = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_length=200
)

llm = HuggingFacePipeline(pipeline=pipe)

# Retrieval QA
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever()
)

# Chat loop
while True:

    question = input("Ask Question: ")

    response = qa.invoke(question)

    print("\nAnswer:")
    print(response["result"])