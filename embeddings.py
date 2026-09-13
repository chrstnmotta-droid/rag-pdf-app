from dotenv import load_dotenv
import os
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_chunks(chunked_text: dict):
    load_dotenv()
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    embeddings_by_doc = {}
    for pdf, chunks in chunked_text.items():
        embedding_chunks = []
        for i in chunks:
            response = client.embeddings.create(
            input= i, model = "text-embedding-3-small"
            )
            embedding_chunks.append(response.data[0].embedding)
        embeddings_by_doc[pdf]= embedding_chunks
    return embeddings_by_doc




