import streamlit as st

def resume_form():
    with st.form("resume_form", clear_on_submit=False):
        name = st.text_input("Full Name *", placeholder="John Doe")
        email = st.text_input("Email Address *", placeholder="john.doe@email.com")
        phone = st.text_input("Phone Number *", placeholder="+1 (555) 123-4567")
        
        education = st.text_area(
            "Education *", 
            placeholder="Bachelor of Science in Computer Science\nUniversity of Technology, 2020",
            height=100
        )
        
        experience = st.text_area(
            "Work Experience *", 
            placeholder="Software Developer | Tech Corp | 2020-2023\n• Developed web applications\n• Led team projects",
            height=150
        )
        
        skills = st.text_area(
            "Skills *", 
            placeholder="Python, JavaScript, React, Node.js, SQL, Git",
            height=100
        )
        
        job_field = st.selectbox(
            "Target Job Field *", 
            ["Software Engineering", "Data Science", "Marketing", "Finance", "Other"]
        )
        submitted = st.form_submit_button("🚀 Generate Resume", use_container_width=True)
    return name, email, phone, education, experience, skills, job_field, submitted
