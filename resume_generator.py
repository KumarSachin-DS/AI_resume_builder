import streamlit as st
from config import llm, embeddings
from vectorstore import initialize_vectorstore
from prompt_templates import prompt_template

vectorstore = initialize_vectorstore(embeddings)

@st.cache_resource
def setup_custom_chain(_llm, _vectorstore, _embeddings):
    try:
        retriever = _vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
        return retriever
    except Exception as e:
        st.error(f"Failed to initialize retriever: {str(e)}")
        st.stop()

retriever = setup_custom_chain(llm, vectorstore, embeddings)

def generate_resume_content(user_details, job_field):
    try:
        query = f"Resume template for {job_field}"
        docs = retriever.get_relevant_documents(query)
        template_content = docs[0].page_content if docs else "Generic resume template."

        formatted_prompt = prompt_template.format(
            user_details=user_details,
            job_field=job_field,
            context=template_content
        )
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating resume: {str(e)}")
        return None
