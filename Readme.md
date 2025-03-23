# Gen AI-Driven Cover Letter and Cold Email Generator for Job Applications

## Introduction
In today's fast-paced job market, applicants face the challenge of creating personalized, professional cover letters and cold emails for every opportunity—a process that can be both time-intensive and inconsistent. Leveraging generative AI, this project simplifies and enhances the application process by creating tailored cover letters and cold emails based on job descriptions and user-uploaded resumes. By combining resume relevance analysis, professional document formatting, and a user-friendly interface, the system provides high-quality outputs in minimal time.

---

## Problem Statement
The job application process is often time-consuming and repetitive, requiring applicants to craft unique cover letters and cold emails for each role. Personalized cold emails can improve the chances of securing an interview but are labor-intensive to create. Moreover, formatting and ensuring professional design further complicates the process.

**Key Challenges**:
- Crafting unique, personalized documents for every job application.
- Reaching out to hiring managers with relevant and professional content.
- Maintaining high-quality formatting and relevance.

**Solution**:
A system that automates and streamlines the workflow, delivering professional and personalized documents efficiently.

---

## Objectives
- Automate the creation of personalized cover letters and cold emails.
- Ensure document relevance through resume analysis.
- Provide a user-friendly interface for ease of use.
- Generate professionally formatted Word documents.

---

## System Design and Architecture

**Input**:  
- User uploads a resume and enters a job posting URL.

**Processing**:
1. Scrape job descriptions from the URL.
2. Match the uploaded resume to job requirements using relevance scoring.
3. Generate the document using LLMs (e.g., Google Gemini via LangChain).

**Output**:  
A polished Word document featuring:
- Tailored Cover Letter.

### Flowchart
_Figure 1: Project Flowchart_

---

## Key Technologies
- **Frontend**: Streamlit for the user interface.
- **Backend**: Python with LangChain.
- **LLM**: gemini-2.0-pro-exp-02-05 via Google API.
- **File Processing**: `python-docx` for Word generation.
- **Data Cleaning**: Regular expressions for preprocessing.

---

## Features
### 1. **Dynamic Cover Letter Creation**
- Incorporates details from uploaded resumes and job descriptions.
- Includes clickable contact links and professional headers.

### 2. **Cold Email Generation**
- Tailors content to job postings.
- Highlights the user’s skills effectively.

### 3. **User-Friendly Interface**
- Simplified input and output process via Streamlit.


---

## Implementation
1. **Input**: Resume and job posting URL.
2. **Text Extraction**:
   - **Resume**: Processed using `python-docx` or `PyPDF2`.
   - **Job Description**: Scraped and cleaned using LangChain's `WebBaseLoader`.
3. **Matching**:
   - Resume content matched to job requirements via Gemini + prompt.
4. **Content Generation**:
   - Prompts structured for LLMs to create cover letters or emails.
5. **Output**:
   - Cover Letter Documents formatted and saved as `.docx` files.

---

## Results
- **Cover Letters**: Tailored and professional, saving users time.
- **Cold Emails**: Polished tone emphasizing relevant skills.
- **User Feedback**: Highlights the ATS score of the given resume and reccomendations.

_Figures:_
- Streamlit-based UI
- Cold Email Generation
- Cover Letter Generation with download options

---

## Challenges
- Handling diverse file formats for resume uploads.
- Ensuring relevance when matching resumes to job descriptions.
- Maintaining prompt quality for consistent LLM responses.

---

## Conclusion
The AI-Driven Cover Letter and Cold Email Generator successfully automates the application process, producing professional documents with minimal effort. Future improvements include:
- Expanding file format support.
- Enhancing the user interface.
- Integrating additional AI models for better accuracy.
- Generating a Resume that matches the job description.
- Features that utilize internal advocates that may refer the user into the output.

---

## Lessons Learned
Inspired by a statement from Naresh Jasotani, "Start with projects that solve your problem," We embarked on this journey to help make the modern job search easier. Through trial and error, We integrated LLMs, Features, and project implementation using free resources on the internet. The journey was challenging but rewarding, teaching us the value of pursuing meaningful work.

---

## Acknowledgements
Special thanks to the creator of the YouTube tutorial **"AI Cold Email Generator"** for foundational insights. Building on this knowledge, we added:
- Cover letter generation.
- Dynamic output tailored to job descriptions and resumes.

---

## References
- **Python Libraries**: LangChain, Streamlit, `python-docx`, PyPDF2.
- **AI Models**: gemini-2.0-pro-exp-02-05 by Google.
- [YouTube Tutorial](https://youtu.be/CO4E_9V6li0?si=PAuaHRUFBV3BsIpK)

---

## Instructions
1. **Download and Save the Project**: `ATS Ninjas`
2. Install Anaconda and create a conda environment
3. cd to App and run pip install -r requrements.txt
4. **Run the Project**:
   streamlit run main.py
