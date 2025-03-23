import os
import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="resource/my_portfolio.csv"):
        self.file_path = file_path

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Portfolio CSV not found at: {file_path}\n"
                "Ensure that the file is placed in the 'resource' directory relative to the script, "
                "or provide the correct path."
            )

        print(f"Loading portfolio data from: {file_path}")
        self.data = pd.read_csv(file_path)

        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        current_count = self.collection.count()
        print(f"Collection count before loading: {current_count}")

        if current_count == 0:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )
            print("Portfolio data successfully loaded into the collection.")
        else:
            print("Collection already has data; skipping load.")

    def query_links(self, skills, resume_content=None):
        if resume_content:
            relevant_skills = self.extract_relevant_skills(resume_content)
            skills += relevant_skills

        print(f"Querying links for skills: {skills}")
        results = self.collection.query(query_texts=skills, n_results=2)

        if not results.get("metadatas"):
            print("No metadata returned. Make sure the collection is loaded correctly.")
            return []

        return [item["links"] for item in results["metadatas"]]

    def extract_relevant_skills(self, resume_content):
        # Placeholder for actual NLP logic
        print("Extracting relevant skills from resume content...")
        return ["skill_from_resume"]
