# Plan Pseudocode: 
# receive query as string -> 
# embed query with OpenAI in the exact same way as the chunks ->
#  use embedded query retrieve through chroma database top 5 chunks (vectors) based on cosine similarity (use doc quary and get chromadb)
from vector_database import collection

def embed_query(query):
    load_dotenv()
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input= query, model = "text-embedding-3-small"
        )
    embedding_query = response.data[0].embedding
    return embedding_query

def retrieval_top_5k(query):
    embedding_query = embed_query(query)
    top_5k = collection.query(
        query_embeddings = [embedding_query],
        n_results = 5
    )
    return top_5k
