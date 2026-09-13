from datetime import datetime
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(settings = Settings(allow_reset = True))
collection = client.get_or_create_collection(
    name="file_chunks",
    metadata={"description": "Chunked and embedded text from uploaded PDFs for RAG retrieval"}
)

def store_embeddings(embeddings_by_doc: dict, chunks_by_doc: dict, collection):
    for pdf, chunks in chunks_by_doc.items():
        ids = [f"{pdf}_{i}" for i in range(len(chunks))]
        metadata = [{"source": pdf} for _ in chunks]
        collection.add(
            ids = ids,
            documents = chunks,
            embeddings = embeddings_by_doc[pdf],
            metadatas = metadata
        )


