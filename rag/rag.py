import os
from openai import OpenAI
import torch
from torch import Tensor
from dotenv import load_dotenv
from utils.config_loader import load_config
load_dotenv()

config = load_config()


def cosine_similarity(a:Tensor,b:Tensor)->float:
    """function for finding similarity"""
    if not isinstance(a,Tensor):
        a = torch.Tensor(a)
    if not isinstance(b,Tensor):
        b = torch.Tensor(b)
    return float(torch.nn.functional.cosine_similarity(a.unsqueeze(0)))