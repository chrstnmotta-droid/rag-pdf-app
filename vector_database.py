from datetime import datetime
from embeddings import embed_chunks
import chromadb

client = chromadb.PersistentClient()
collection = client.get_or_create_collection(
    name="file_chunks",
    metadata={"description": "Chunked and embedded text from uploaded PDFs for RAG retrieval"}
)

def store_embeddings(file, collection):
    chunks, vectors = embed_chunks(file)
    ids = [f"{file}_{i}" for i in range(len(chunks))]
    metadata = [{"source": file} for _ in chunks]

    collection.add(
        ids = ids
        documents = chunks
        embeddings = vectors
        metadatas = metadata
    )


