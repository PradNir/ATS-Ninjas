import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from gemini_client import GeminiClient
from utils import clean_text

import base64

import base64

def add_custom_css():
    video_path = "static/ninja_bg.mp4"
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        base64_video = base64.b64encode(video_bytes).decode()

    st.markdown(f"""
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap" rel="stylesheet">

        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow-x: hidden;
                background-color: transparent;
            }}

            .stApp {{
                position: relative;
                width: 100vw;
                height: 100vh;
                overflow-x: hidden;
            }}

            .block-container {{
                max-width: 100%;
                padding: 2rem 5vw;
                margin: 0 auto;
                background-color: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                color: white;
            }}

            .video-bg {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                object-fit: cover;
                z-index: -1;
                opacity: 0.3;
            }}

            h1 {{
                font-family: 'Roboto', sans-serif;
                font-weight: 700;
                font-size: 2.6rem;
                color: #00BFFF;
                text-align: center;
                margin-bottom: 2rem;
            }}

            .stTextInput, .stFileUploader, .stSelectbox, .stButton>button {{
                font-size: 1rem;
            }}

            .stButton>button {{
                background-color: #00BFFF;
                color: white;
                border-radius: 8px;
                padding: 0.5rem 1.2rem;
            }}
        </style>

        <video autoplay muted loop class="video-bg">
            <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
        </video>
    """, unsafe_allow_html=True)



def create_streamlit_app(llm, clean_text):
    st.set_page_config(layout="wide", page_title="ATS Ninja", page_icon="📧")
    add_custom_css()

    st.title("📧 ATS Ninja: GEN-AI Powered Job Application Assistant")

    url_input = st.text_input("🔗 Job Posting URL", value="")

    resume_file = st.file_uploader("📄 Upload Your Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    content_type = st.selectbox(
        "✍️ What do you want to generate?",
        ["Cold Email", "Cover Letter", "ATS Analyzer"]
    )

    submit_button = st.button("🚀 Generate")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            raw_text = loader.load().pop().page_content
            job_description = clean_text(raw_text[:6000])

            resume_content = ""
            if resume_file:
                if resume_file.type == "application/pdf":
                    resume_content = extract_pdf_text(resume_file)
                elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_content = extract_docx_text(resume_file)
                elif resume_file.type == "text/plain":
                    resume_content = resume_file.read().decode("utf-8")

            if content_type == "ATS Analyzer":
                if not resume_content:
                    st.error("Please upload a resume for ATS analysis.")
                    return

                ats_results = llm.calculate_ats_score(resume_content, job_description)

                st.markdown("### 📊 ATS Compatibility Analysis")
                st.metric(label="ATS Score (%)", value=f"{ats_results['ats_score']}%")
                st.markdown("#### ✅ Matched Keywords")
                st.success(", ".join(ats_results['matched_keywords']))
                st.markdown("#### ⚠️ Missing Keywords")
                st.warning(", ".join(ats_results['missing_keywords']))
                st.markdown("#### 🚀 Recommendations")
                for rec in ats_results['recommendations']:
                    st.write(f"- {rec}")

            elif content_type == "Cold Email":
                email_content = llm.write_mail(job_description, "no links")
                st.markdown("### ✉️ Generated Cold Email:")
                st.code(email_content, language='markdown')

            elif content_type == "Cover Letter":
                if not resume_content:
                    st.error("Please upload your resume for the cover letter.")
                    return

                cover_letter_content = llm.write_cover_letter(resume_content, job_description, "no links")
                st.markdown("### 📝 Generated Cover Letter:")
                st.code(cover_letter_content, language='markdown')

                filename = llm.save_cover_letter(cover_letter_content)
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📥 Download Cover Letter",
                        data=file,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        except Exception as e:
            st.error(f"❌ An Error Occurred: {e}")

def extract_pdf_text(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    return "".join(page.extract_text() for page in reader.pages)

def extract_docx_text(docx_file):
    from docx import Document
    doc = Document(docx_file)
    return "\n".join(para.text for para in doc.paragraphs)

if __name__ == "__main__":
    chain = GeminiClient()
    create_streamlit_app(chain, clean_text)
