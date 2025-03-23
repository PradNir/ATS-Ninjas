import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from gemini_client import GeminiClient
from utils import clean_text

def create_streamlit_app(llm, clean_text):
    st.title("📧 Cold Mail & Cover Letter Generator")
    url_input = st.text_input("Enter a Job Posting URL:", value="")

    # Upload Resume File
    resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])

    # Dropdown to choose content type
    content_type = st.selectbox("Select Content Type", ["Cold Email", "Cover Letter"])

    submit_button = st.button("Generate Content")

    if submit_button:
        try:
            # 1) Load and clean web content
            loader = WebBaseLoader([url_input])
            raw_text = loader.load().pop().page_content
            data = clean_text(raw_text[:6000])  # limit text for safety

            # 2) Parse resume if provided
            if resume_file is not None:
                if resume_file.type == "application/pdf":
                    resume_content = extract_pdf_text(resume_file)
                elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_content = extract_docx_text(resume_file)
                elif resume_file.type == "text/plain":
                    resume_content = str(resume_file.read(), "utf-8")
                else:
                    st.error("Unsupported resume format")
                    return
            else:
                resume_content = ""

            # 3) Extract jobs
            jobs = llm.extract_jobs(data)

            with st.expander("🔍 View Extracted Jobs (Raw JSON)"):
                st.json(jobs)

            # Handle no jobs
            if not jobs or (isinstance(jobs, list) and len(jobs) == 0):
                st.warning("No job postings extracted. Try a different URL.")
                return

            # Flatten if nested
            flat_jobs = []
            for job_item in jobs:
                if isinstance(job_item, list):
                    flat_jobs.extend(job_item)
                else:
                    flat_jobs.append(job_item)
            jobs = flat_jobs

            # 4) Generate Content
            for job in jobs:
                # For demonstration, let's do a direct “job_description”
                job_description = job.get("description", "No description found")

                if content_type == "Cold Email":
                    content = llm.write_mail(job_description, "no links")
                    st.code(content, language='markdown')

                elif content_type == "Cover Letter":
                    content = llm.write_cover_letter(resume_content, job_description, "no links")
                    st.code(content, language='markdown')

                    # (Optional) No docx saving? Or keep it:
                    filename = llm.save_cover_letter(content)
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="Download Cover Letter",
                            data=file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

# Helper: Extract PDF text
def extract_pdf_text(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Helper: Extract DOCX text
def extract_docx_text(docx_file):
    from docx import Document
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

if __name__ == "__main__":
    chain = GeminiClient()  # from gemini_client.py
    st.set_page_config(layout="wide", page_title="Cold Email & Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)
