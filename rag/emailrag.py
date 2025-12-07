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
    

