import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from gemini_client import GeminiClient
from utils import clean_text

def create_streamlit_app(llm, clean_text):
    st.title("📧 ATS Compatibility Analyzer & Content Generator")
    
    url_input = st.text_input("Enter a Job Posting URL:", value="")

    # Resume upload (optional but needed for ATS analyzer)
    resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])

    # Dropdown: Cold Email, Cover Letter, ATS Analyzer
    content_type = st.selectbox(
        "Select Content Type",
        ["Cold Email", "Cover Letter", "ATS Analyzer"]
    )

    submit_button = st.button("Generate Content")

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

            # ATS Analyzer logic
            if content_type == "ATS Analyzer":
                if not resume_content:
                    st.error("Please upload a resume for ATS analysis.")
                    return

                ats_results = llm.calculate_ats_score(resume_content, job_description)

                st.header("🔍 ATS Compatibility Analysis")
                st.metric(label="ATS Score (%)", value=f"{ats_results['ats_score']}%")

                st.subheader("✅ Matched Keywords")
                st.write(", ".join(ats_results['matched_keywords']))

                st.subheader("⚠️ Missing Keywords")
                st.write(", ".join(ats_results['missing_keywords']))

                st.subheader("🚀 Recommendations")
                for rec in ats_results['recommendations']:
                    st.write(f"- {rec}")

            # Cold Email generation logic
            elif content_type == "Cold Email":
                email_content = llm.write_mail(job_description, "no links")
                st.markdown("### Generated Cold Email:")
                st.code(email_content, language='markdown')

            # Cover Letter generation logic
            elif content_type == "Cover Letter":
                if not resume_content:
                    st.error("Please upload your resume for the cover letter.")
                    return
                
                cover_letter_content = llm.write_cover_letter(resume_content, job_description, "no links")
                st.markdown("### Generated Cover Letter:")
                st.code(cover_letter_content, language='markdown')

                # Save cover letter as Word doc
                filename = llm.save_cover_letter(cover_letter_content)
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download Cover Letter",
                        data=file,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

# Helper functions for PDF and DOCX extraction
def extract_pdf_text(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_docx_text(docx_file):
    from docx import Document
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

if __name__ == "__main__":
    chain = GeminiClient()
    st.set_page_config(layout="wide", page_title="ATS Compatibility Analyzer & Content Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)
