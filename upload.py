import os
import re
import json
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader

def convert_pdf_to_text():
    """function to convert PDF to text and append content to vault text"""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        with open(file_path,'r') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                if page.extract_text():
                    text += page.extract_text() + ""

            #normalize the white spcace
            text = re.sub(r'\s+',' ',text).strip()
            #split the text into chunks by sentences, repecting a maximun chunck size
            sentences = re.split(r'(?<=[.!?]) +',text)#split on spaces following sentenceending punctuation
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                #check if the current sentence plus the current chunks size exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            with open("vault_text", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    #write each chunk to its own line
                    vault_file.write(chunk.strip() + "\n")
            print("PDF content appended to vault.txt with each chunk on a separate line.")




            