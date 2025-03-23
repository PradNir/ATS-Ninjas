import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail & Cover Letter Generator")
    url_input = st.text_input("Enter a Job Posting URL:", value="")


    # Upload Resume File
    resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])

    # Dropdown to choose content type
    content_type = st.selectbox("Select Content Type", ["Cold Email", "Cover Letter"])

    submit_button = st.button("Generate Content")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()

            # Load resume content
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

            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                
                # Generate based on selected content type
                if content_type == "Cold Email":
                    content = llm.write_mail(job, links)
                    st.code(content, language='markdown')
                elif content_type == "Cover Letter":
                    content = llm.write_cover_letter(resume_content, job, links)
                    st.code(content, language='markdown')

                    # Save as Word document
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


# Helper function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Helper function to extract text from a DOCX file
def extract_docx_text(docx_file):
    from docx import Document
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email & Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
