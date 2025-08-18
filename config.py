import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@st.cache_resource
def initialize_components():
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, timeout=120)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return llm, embeddings
    except Exception as e:
        st.error(f"Failed to initialize LLM or embeddings: {str(e)}")
        st.stop()

llm, embeddings = initialize_components()
