from pdf_utiliz import extract_pdf, chunk_text
from dotenv import load_dotenv
import os
from openai import OpenAI
EMBEDDING_MODEL = "text-embedding-3-small"

def embed_chunks(file):
    load_dotenv()
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    embedding_chunks = []
    pdf_text = extract_pdf(file)
    chunks = chunk_text(pdf_text)

    for i in chunks:
        response = client.embeddings.create(
            input= i, model = "text-embedding-3-small"
        )
        embedding_chunk = response.data[0].embedding
        embedding_chunks.append(embedding_chunk)
        
    return chunks, embedding_chunks 




