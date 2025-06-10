# genzway_chatbot_streamlit.py

import os
import pandas as pd
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st # Import Streamlit

# --- Configuration for Streamlit Page ---
st.set_page_config(
    page_title="GenZway Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 GenZway Chatbot")
st.markdown("Ask me anything about GenZway! I'll provide answers based on the `content_detail.csv` file.")

# === Load your data (CSV or static content) ===
@st.cache_resource # Cache the loading of content and vector store to avoid re-running on each interaction
def setup_knowledge_base():
    if not os.path.exists("content_detail.csv"):
        st.error("Error: Please create 'content_detail.csv' with the GenZway paragraph in the same directory.")
        st.stop() # Stop the app if file is missing

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
        st.success("Vector store created/updated with GenZway content.")
    else:
        st.info("Using existing GenZway vector store.")

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

    return retriever, chain

# Setup the knowledge base once
retriever, chain = setup_knowledge_base()

# === Chatbot Logic for Streamlit ===

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your question about GenZway..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        # Retrieve relevant content
        reviews = retriever.invoke(prompt)
        
        # Invoke the LLM chain
        result = chain.invoke({"reviews": reviews, "question": prompt})
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(result)