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


def chat_with_gpt(user_input,system_message,vault_embeddings,vault_content,model,converstion_history,client):
    """function to interact with OpenAI model"""
    relevant_context = get_revelant_context(user_input,vault_embeddings_tensor,vault_content,client,top_k=3)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print("Context pulled from documents: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "No relevant context found." + RESET_COLOR)

    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = f"Context:\n{context_str}\n\nQuestion: {user_input}"

    #append user input to the convertion history
    converstion_history.append({"role":"user","content": user_input_with_context})
    messages = [{"role":"system","context":user_input_with_context}]
    response = client.chat.completions.create(
        model = model,messages=messages,temperature = 0.7,max_tokens = 1000
    )
    converstion_history.append(
        {"role":"assistant","content":response.choices[0].message.content}
    )
    return response.choices[0].message.content

#parse command-line
parser = argparse.ArgumentParser(description="ChatGPT RAG System")
parser.add_argument(
    "--model",
    default="gpt-3.5-turbo",
    help = "Openai model to use (default: gpt-3.5-turbo)"
)
args = parser.parse_args()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#load the vault content
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding="utf-8") as vault_file:
        vault_content = vault_file.readlines()

#geberating embeddings and converting them to tensors
print("Generating embeddings for vault content...")
vault_embeddings = []
for content in vault_content:
    if content.strip():
        response = client.embeddings.create(model="text-embedding-ada-002",input=content)
        vault_embeddings.append(response.data[0].embedding)

vault_embeddings_tensor = torch.tensor(vault_embeddings)
print("Embeddings generated successfully")


#converstion loop
conversation_history = []
system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text"


print(PINK + "\nWelcome to the RAG Chat System!" + RESET_COLOR)
print(CYAN + "Type 'quit' to exit the chat." + RESET_COLOR)

while True:
        user_input = input(YELLOW + "\nAsk a question about your documents: " + RESET_COLOR)
        if user_input.lower() == "quit":
            break

        try:
            response = chat_with_gpt(
                user_input,
                system_message,
                vault_embeddings_tensor,
                vault_content,
                args.model,
                conversation_history,
                client,
            )
            print(NEON_GREEN + "\nResponse: \n\n" + response + RESET_COLOR)
        except Exception as e:
            print(f"An error occurred: {str(e)}")


