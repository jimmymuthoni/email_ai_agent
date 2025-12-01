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


def upload_txtfile():
    """function to upload text file and appand its content to vault.txt"""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path,'r',encoding="utf-8") as txt_file:
            text = txt_file.read()
            #normalize the white space ans clean up the sapce
            text = re.sub(r's\+',' ',text).strip()
            #split text into chunks by sentences, repecting a maximum chuck size
            sentences = re.split(r'(?<=[.!?]) +',text)# split on spaces following sentence-ending punctuation
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                 # Check if the current sentence plus the current chunk exceeds the limit
                if len(sentence) + len(current_chunk) + 1 < 1000: # +1 for the space
                     current_chunk += (sentence + " ").strip()
                else:
                    #when chunk exceed 1000 characters, store it and start a new one
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            with open("vault_text", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")

            print("Text file content appended to vault.text with each chunk on a separate line.")


def upload_json_file():
    """function to upload json file and aapend the content to vault.txt"""
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path,'r', encoding="utf-8") as json_file:
            data = json.load(json_file)

            #flattening json file content into  asingle string
            text = json.dumps(data,ensure_ascii=False)

            #normalize the whitespsce and clean up he text
            text = re.sub(r'\s+','',text).strip()

            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")  # Two newlines to separate chunks

            print(f"JSON file content appended to vault.txt with each chunk on separate line.")

#main window
root = tk.Tk()
root.title("Upload ---> .pdf, .txt or .json file")

#button to open the files in different format
pdf_button = tk.Button(root,text="Upload PDF",command=convert_pdf_to_text)
pdf_button.pack(padx=10)
text_button = tk.Button(root,text="Upload Text File",command=upload_txtfile)
text_button.pack(padx=10)
json_button = tk.Button(root,text="Upload JSON",command=upload_json_file)
json_button.pack(padx=10)

#main event loop
root.mainloop()




                
            
                     
                     







            