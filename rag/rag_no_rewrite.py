import os
import torch
from openai import OpenAI
import argparse
from dotenv import load_dotenv
from utils.config_loader import load_config
load_dotenv()

#ANSI escape codes for colors
PINK = "\033[95m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
NEON_GREEN = "\n033[92m"
RESET_COLOR = "\033[0m"

def open_file(file_path):
    """this finction opens file and return its content"""
    with open(file_path,'r',encoding="utf-8") as infile:
        return infile.read()

def get_revelant_context(rewtitten_input,vault_embeddings,vault_content,client,top_k =3):
    """this function gets relevant context from the vault based on user input"""
    if vault_embeddings.nelement() == 0:
        return []
    response = client.embeddings.create(
        model = "text-embedding-ada-002", input = rewtitten_input
    )
    input_embedding = response.data[0].embedding

    cos_score = torch.cosine_similarity(
        torch.tensor(input_embedding).unsqueeze(0), vault_embeddings
    )
    top_k = min(top_k, len(cos_score))
    top_indicies = torch.topk(cos_score,k=top_k)[1].tolist()
    relevant_context = [vault_content[idx].strip() for idx in top_indicies]
    return relevant_context


