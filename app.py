# genzway_chatbot.py

import os
import pandas as pd
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# === Load your data (CSV or static content) ===
if not os.path.exists("content_detail.csv"):
    raise FileNotFoundError("Please create 'content_detail.csv' with the GenZway paragraph.")

with open("content_detail.csv", "r", encoding="utf-8") as f:
    content = f.read()

# === Create LangChain Documents ===
documents = [Document(page_content=content, metadata={"source": "GenZwayOverview"}, id="1")]

# === Embedding Setup ===
embedding = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "genzway_vector_db"
add_documents = not os.path.exists(db_location)

vectorstore = Chroma(
    collection_name="genzway_knowledge",
    persist_directory=db_location,
    embedding_function=embedding
)

if add_documents:
    vectorstore.add_documents(documents=[documents[0]], ids=["1"])

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# === LLM Chain Setup ===
llm = OllamaLLM(model="llama3.2")

template = """
You are a helpful assistant answering questions based on the following content:

{reviews}

Now answer this user question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

# === CLI Chatbot Loop ===
while True:
    print("\n-----------------------------")
    question = input("Ask your question (or 'q' to quit): ").strip()
    if question.lower() == 'q':
        break

    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print("\n🤖 Answer:\n", result)
