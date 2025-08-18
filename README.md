# 🚀 AI Resume Builder

## Overview

**AI Resume Builder** is a user-friendly, Streamlit-powered web application for creating professional, ATS-friendly resumes. It leverages OpenAI’s powerful GPT models and the LangChain toolkit to help you generate, format, and export polished resumes as PDF files, tailored to your field and experience.

- Supports multiple job types and fields
- Uses FAISS-powered semantic search for template matching
- Offers easy download of resumes in PDF format
- Can include a profile photo on your resume

---

## ✨ Features

- Intelligent resume generation using OpenAI GPT
- Fixed structured PDF template with consistent, professional layout
- Resume templates for fields like Software Engineering, Data Science, Marketing, Finance
- Easy PDF download functionality
- Add profile photo to your resume (optional)

---

## Demo

![AI Resume Builder Screenshot]([./assets/demo_screenshot.png](https://github.com/KumarSachin-DS/AI_resume_builder/blob/main/Demo_screenshot.png))  
*Screenshot of the app UI. Update this path when you add your own screenshot.*

---

## 📦 Getting Started

### Prerequisites

- **Python 3.8 or later**
- An [OpenAI API key](https://platform.openai.com/signup/) (with access to GPT-4o-mini)

### Installation

1. **Clone the repository:**
git clone https://github.com/yourusername/ai_resume_builder.git
cd ai_resume_builder

2. **(Recommended) Create a virtual environment:**
- python -m venv venv
- source venv/bin/activate # on macOS/Linux
- venv\Scripts\activate # on Windows

3. **Install dependencies:**
-pip install -r requirements.txt

4. **Set up your OpenAI API key:**

Create a `.env` file in the root directory and add:
- OPENAI_API_KEY=your_openai_api_key_here

---

## Usage

1. **Launch the app:**
streamlit run app.py
2. **Fill out the information form:**  
(Name, Contact, Experience, Education, Skills, Summary)

3. **Upload a profile photo (optional):**
- Click the “Upload Photo” button in the app to add your picture to the generated resume.

4. **Preview your resume and download as PDF.**
---

## 🛠 Troubleshooting

- If you receive an error relating to API keys, ensure your `.env` file is set up and loaded.
- If PDF download fails, check that you have write permissions in your working directory.

---
## 📜 License
- This project is licensed under the MIT License. Feel free to use and adapt!
