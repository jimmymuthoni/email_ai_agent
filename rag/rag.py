import os
import json
from openai import OpenAI
from typing import List
import torch
from torch import Tensor
from dotenv import load_dotenv
from utils.config_loader import load_config
load_dotenv()




def cosine_similarity(a:Tensor,b:Tensor)->float:
    """function for finding similarity"""
    if not isinstance(a,Tensor):
        a = torch.Tensor(a)
    if not isinstance(b,Tensor):
        b = torch.Tensor(b)
    return float(torch.nn.functional.cosine_similarity(a.unsqueeze(0)))


class LocalRAG:
    """class to perform RAG implementation"""
    def __init__(self):
        self.config = load_config()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.load_vault()

    def load_vault(self):
        """method to load vault content,check embeddings,generate if not generate,load them, convert them to tensor"""
        #check if the vault path exists
        if not os.path.exists(self.config['vault_file']):
            raise FileNotFoundError(f"vault file {self.config['vault_file']} not found.Create it first")
        #load the text content
        with open(self.config['vault_file'], 'r', encoding="utf-8") as file:
            self.vault_text = file.read().split("\n")
        #check embeddings, generate embeddings if they are not found
        if not os.path.exists(self.config['embeddings_file']):
            raise FileNotFoundError("Embeddings file not found.Generating embeddings....")
            self.generate_embeddings()

        #load the embeddings
        with open(self.config['embeddings_file']) as file:
            self.embeddings = json.load(file)
        #convert embeddings to tensor
        self.embeddings_tensor = torch.tensor(self.embeddings)

    def generate_embeddings(self):
        """generate embeddings for vault content"""
        print("Generating embeddings......")
        embeddings = []
        for i, text in enumerate(self.vault_text):
            reponse = self.client.embeddings.create(model="text-embedding-ada-002",input=text)
            embeddings.append(reponse.data[0].embedding)
            if (i + 1) % 10 == 0:
                print(f"Processed {i+1} lines...")
        #save the embeddings
        with open(self.config['embeddings_file'],'w') as file:
            json.dump(embeddings,file)
        print("Embeddingd generated and saved successfully!")
    
    def get_embedding(self,text:str)->List[float]:
        """get embeddings using OpenAI model"""
        response = self.client.embeddings.create(model="text-embedding-ada-002",input=text)
        return response.data[0].embedding
            
        

        