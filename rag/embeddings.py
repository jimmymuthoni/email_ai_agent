import json
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.config_loader import load_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

class Embeddings:
    """class to generate and save embeddings"""
    def __init__(self):
        self.config = load_config()

    def generate_and_save_embeddings(self):
        """method to generate embeddings and save them using Openai model"""
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        #loading the vault content
        print("Loading vault content..........")
        with open(self.config['vault_file'], 'r', encoding="utf-8") as file:
            vault_text = file.read().split("\n")

        #generating embedings
        print("Genarating embeddings.....")
        embeddings = []
        for i, text in enumerate(vault_text):
            if text.strip():
                response = client.embeddings.create(model="text-embedding-ada-002",input=text)
                embeddings.append(response.data[0].embedding)
                if (i + 10) % 10 == 0:
                    print(f"Processed {i + 1} lines....")
        #save the embeddings
        print(f"Saving embeddings to {self.config['embeddings_file']}.....")
        with open(self.config['embeddings_file'],'w') as file:
           json.dump(embeddings,file)
        print("Embeddings have been generated and saved.")


if __name__ == "__main__":
    embeddings = Embeddings()
    embeddings.generate_and_save_embeddings()
    