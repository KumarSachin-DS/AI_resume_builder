from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import streamlit as st

@st.cache_resource
def initialize_vectorstore(_embeddings):
    try:
        vectorstore = FAISS.load_local(
            folder_path="./faiss_index",
            embeddings=_embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    except (FileNotFoundError, Exception):
        sample_templates = [ 
            Document(
                page_content="""
                PROFESSIONAL SUMMARY
                Innovative Software Engineer with 5+ years of experience in full-stack development, specializing in Python, Java, and cloud technologies. Proven track record of delivering scalable solutions and leading cross-functional teams.

                EXPERIENCE
                Senior Software Developer | XYZ Corporation | 2020-2023
                • Developed and maintained web applications using Python Django and React
                • Led a team of 4 developers in delivering critical business applications
                • Implemented CI/CD pipelines reducing deployment time by 40%

                Software Developer | ABC Tech | 2018-2020
                • Built RESTful APIs handling 10,000+ daily requests
                • Collaborated with product teams to define technical requirements
                • Optimized database queries improving performance by 25%

                EDUCATION
                Bachelor of Science in Computer Science | University Name | 2018

                TECHNICAL SKILLS
                Languages: Python, Java, JavaScript, SQL
                Frameworks: Django, React, Spring Boot
                Tools: Git, Docker, AWS, Jenkins
                """,
                metadata={"job_field": "Software Engineering"}
            ),
            Document(
                page_content="""
                PROFESSIONAL SUMMARY
                Data-driven Data Scientist with expertise in machine learning, statistical analysis, and big data technologies. Experienced in transforming complex datasets into actionable business insights.

                EXPERIENCE
                Senior Data Scientist | DataCorp Inc | 2019-2023
                • Developed predictive models improving customer retention by 15%
                • Analyzed large datasets using Python, R, and SQL
                • Created data visualization dashboards for executive reporting

                Data Analyst | Analytics Solutions | 2017-2019
                • Performed statistical analysis on customer behavior data
                • Built automated reporting systems using Python
                • Collaborated with marketing teams on campaign optimization

                EDUCATION
                Master of Science in Data Science | University Name | 2017
                Bachelor of Science in Statistics | University Name | 2015

                TECHNICAL SKILLS
                Languages: Python, R, SQL, Scala
                ML Libraries: Scikit-learn, TensorFlow, PyTorch
                Tools: Jupyter, Tableau, Spark, AWS
                """,
                metadata={"job_field": "Data Science"}
            ),
            Document(
                page_content="""
                PROFESSIONAL SUMMARY
                Results-driven Marketing Professional with 6+ years of experience in digital marketing, brand management, and campaign optimization. Proven ability to increase ROI and drive customer engagement.

                EXPERIENCE
                Marketing Manager | BrandCorp | 2020-2023
                • Managed digital marketing campaigns with $500K+ annual budget
                • Increased website traffic by 60% through SEO and content marketing
                • Led cross-functional teams for product launches

                Digital Marketing Specialist | Growth Agency | 2018-2020
                • Developed social media strategies increasing engagement by 40%
                • Managed PPC campaigns with average ROAS of 4:1
                • Created content marketing strategies for B2B clients

                EDUCATION
                Bachelor of Business Administration in Marketing | University Name | 2018

                CORE SKILLS
                Digital Marketing: SEO, SEM, Social Media, Email Marketing
                Analytics: Google Analytics, Facebook Ads Manager, HubSpot
                Design: Adobe Creative Suite, Canva
                """,
                metadata={"job_field": "Marketing"}
            ),
            Document(
                page_content="""
                PROFESSIONAL SUMMARY
                Detail-oriented Finance Professional with 7+ years of experience in financial analysis, budgeting, and risk management. Strong background in corporate finance and investment analysis.

                EXPERIENCE
                Senior Financial Analyst | FinanceCorp | 2019-2023
                • Conducted financial modeling and valuation analysis for M&A transactions
                • Prepared monthly financial reports and variance analysis
                • Managed annual budgeting process for $50M+ revenue division

                Financial Analyst | Investment Group | 2017-2019
                • Analyzed investment opportunities and prepared due diligence reports
                • Built financial models for portfolio companies
                • Supported quarterly earnings reporting and investor relations

                EDUCATION
                Master of Business Administration in Finance | University Name | 2017
                Bachelor of Science in Accounting | University Name | 2015

                CORE COMPETENCIES
                Financial Analysis: Modeling, Valuation, Budgeting, Forecasting
                Software: Excel, SAP, QuickBooks, Bloomberg Terminal
                Certifications: CFA Level II, FRM
                """,
                metadata={"job_field": "Finance"}
            )
        ]
        vectorstore = FAISS.from_documents(sample_templates, _embeddings)
        try:
            vectorstore.save_local("./faiss_index")
        except Exception as e:
            st.warning(f"Could not save vector store: {e}")
        return vectorstore
