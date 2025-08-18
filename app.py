import os, tempfile
import streamlit as st
from config import OPENAI_API_KEY
from resume_generator import generate_resume_content
from pdf_utils import create_pdf
from ui_components import resume_form

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="wide")
st.title("🤖 AI Resume Builder")
st.markdown("Generate a professional, ATS-friendly resume tailored to your target job field.")

if not OPENAI_API_KEY:
    st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in .env")
    st.stop()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Your Information")
    name, email, phone, education, experience, skills, job_field, submitted = resume_form()

with col2:
    st.subheader("📄 Resume Preview")
    if submitted:
        if not all([name, email, phone, education, experience, skills]):
            st.error("❌ Please fill in all required fields.")
        else:
            user_details = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Education: {education}
            Experience: {experience}
            Skills: {skills}
            """
            with st.spinner("🔄 Generating your resume..."):
                resume_content = generate_resume_content(user_details, job_field)
                if resume_content:
                    st.success("✅ Resume generated successfully!")
                    st.text_area("", resume_content, height=400, disabled=True)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        pdf_filename = tmp_file.name
                    
                    if create_pdf(resume_content, pdf_filename):
                        with open(pdf_filename, "rb") as file:
                            st.download_button("📥 Download Resume PDF", file.read(),
                                               f"{name.replace(' ', '_')}_resume.pdf",
                                               "application/pdf", use_container_width=True)
                        os.unlink(pdf_filename)
                    else:
                        st.error("❌ PDF creation failed.")
    else:
        st.info("👆 Fill in details and click 'Generate Resume'.")
