import torch
import os
import json
from openai import OpenAI
import argparse
import yaml
from dotenv import load_dotenv
from utils.config_loader import load_config

# ANSI escape codes for colors
PINK = "\033[95m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
NEON_GREEN = "\033[92m"
RESET_COLOR = "\033[0m"

#loading the environment variable
load_dotenv()


def open_file(file_path):
    """function to open the file"""
    print("Opening file.....")
    try:
        with open(file_path, 'r', encoding="utf-8") as infile:
            return infile.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    
def load_or_generate_embeddings(vault_content,embeddings_file,client):
    """this function loads embeddings if no embeddings it generate and loads"""
    if os.path.exists(embeddings_file):
        print(f"Loading embeddings from '{embeddings_file}'...")
        try:
            with open(embeddings_file, 'r', encoding="utf-8") as file:
                return torch.tensor(json.load(file))
        except json.JSONDecodeError:
            print(f"Invalid JSON format in embeddings file '{embeddings_file}'.")
            embeddings = []
    else:
        print("No embeddings found. Generating new embeddings")
        embeddings = generate_embeddings(vault_content, client)
        save_embeddings(embeddings, embeddings_file)
    return torch.tensor(embeddings)
    

