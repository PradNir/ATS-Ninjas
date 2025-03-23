import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from gemini_client import GeminiClient
from utils import clean_text

def create_streamlit_app(llm, clean_text):
    st.title("📧 Cold Mail & Cover Letter Generator")
    url_input = st.text_input("Enter a Job Posting URL:", value="")

    # Upload Resume File (optional)
    resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])

    # Choose content type
    content_type = st.selectbox("Select Content Type", ["Cold Email", "Cover Letter"])

    submit_button = st.button("Generate Content")

    if submit_button:
        try:
            # 1) Load & clean page content
            loader = WebBaseLoader([url_input])
            raw_text = loader.load().pop().page_content
            data = clean_text(raw_text[:6000])  # limit text size if you like

            # 2) Parse resume if provided
            if resume_file is not None:
                if resume_file.type == "application/pdf":
                    resume_content = extract_pdf_text(resume_file)
                elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_content = extract_docx_text(resume_file)
                elif resume_file.type == "text/plain":
                    resume_content = str(resume_file.read(), "utf-8")
                else:
                    st.error("Unsupported resume format.")
                    return
            else:
                resume_content = ""

            # 3) Extract jobs from the page
            jobs = llm.extract_jobs(data)

            with st.expander("🔍 View Extracted Jobs (Raw JSON)"):
                st.json(jobs)

            if not jobs or (isinstance(jobs, list) and len(jobs) == 0):
                st.warning("No job postings extracted. Try a different URL.")
                return

            # Optional flattening if you suspect nested job lists
            flat_jobs = []
            for j in jobs:
                if isinstance(j, list):
                    flat_jobs.extend(j)
                else:
                    flat_jobs.append(j)
            jobs = flat_jobs

            # 4) Generate the requested content for each job
            for job in jobs:
                # We'll just pass "no links" as we have no portfolio references
                job_desc = job.get("description", "No description available.")
                
                if content_type == "Cold Email":
                    content = llm.write_mail(job_desc, "no links")
                    st.markdown("### Generated Cold Email:")
                    st.code(content, language='markdown')

                elif content_type == "Cover Letter":
                    content = llm.write_cover_letter(resume_content, job_desc, "no links")
                    st.markdown("### Generated Cover Letter:")
                    st.code(content, language='markdown')

                    # Save cover letter as a Word doc
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

# PDF extraction helper
def extract_pdf_text(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# DOCX extraction helper
def extract_docx_text(docx_file):
    from docx import Document
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

if __name__ == "__main__":
    # Create the GeminiClient instance
    chain = GeminiClient()

    st.set_page_config(layout="wide", page_title="Cold Mail & Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)
