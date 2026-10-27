# Check if done correctly by checking vector_database.collection.count() and actual length of the chunks and the output of retrieval
import pdf_extract_chunking 
import vector_database
import embeddings
import evaluation_retrieval

#Extract pdfs
extracted_text = {}
for i in ["algorithms_value_free.pdf", "clark_2025.pdf", "Creel_Helman_2022.pdf", "fooling_shap.pdf"]:
    extracted_text[i] = pdf_extract_chunking.extract_pdf(i)
    
# Chunk by character_chunking with best configuration
chunked_by_doc = {}
for pdf, text in extracted_text.items():
    chunked_by_doc[pdf] = pdf_extract_chunking.character_chunking(text, 1200 , 120) 

vector_database.client.reset()
vector_database.clean_collection = vector_database.client.get_or_create_collection(name = "clean_collection")
embeddings_by_doc = embeddings.embed_chunks(chunked_by_doc)
vector_database.store_embeddings(embeddings_by_doc, chunked_by_doc, vector_database.clean_collection)
evaluation_retrieval.evaluation_top_5k("character_chunking", 1200, 120)


        

            