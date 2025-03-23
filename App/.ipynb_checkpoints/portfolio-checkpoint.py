import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="C:/Users/pradh/OneDrive/Desktop/Cold Email Generator/App/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills, resume_content=None):
        # If resume content is provided, use it for better matching
        if resume_content:
            # Process and integrate resume content into skills
            relevant_skills = self.extract_relevant_skills(resume_content)
            skills += relevant_skills  # Add resume-related skills to the search query
        
        # Use skills to query the portfolio
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

    def extract_relevant_skills(self, resume_content):
        # Implement logic to extract relevant skills from the resume
        # For now, return a placeholder list of skills
        return ["skill_from_resume"]  # Replace with actual extraction logic

