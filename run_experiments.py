import pdf_extract_chunking 
import vector_database
import embeddings
import evaluation_retrieval

#Extract pdfs
extracted_text = {}
for i in ["algorithms_value_free.pdf", "clark_2025.pdf", "Creel_Helman_2022.pdf", "fooling_shap.pdf"]:
    extracted_text[i] = pdf_extract_chunking.extract_pdf(i)

for method in ["sentence","token","character"]:
    for chunk_size in  [1200, 1600, 2000]:
        for overlap_pct in [0, 0.10, 0.20]:
            overlap = int(chunk_size * overlap_pct)
            chunked_by_doc = {}
            for pdf, text in extracted_text.items():
                if method == "character":
                    chunked_by_doc[pdf] = pdf_extract_chunking.character_chunking(text,chunk_size, overlap)
                elif method == "sentence":
                    chunked_by_doc[pdf] = pdf_extract_chunking.sentence_aware_chunking(text, chunk_size, overlap)
                else:
                    chunked_by_doc[pdf] = pdf_extract_chunking.token_aware_chunking(text, chunk_size, overlap)
            vector_database.client.reset()
            vector_database.collection = vector_database.client.get_or_create_collection(name = "clean_collection")
            embeddings_by_doc = embeddings.embed_chunks(chunked_by_doc)
            vector_database.store_embeddings(embeddings_by_doc, chunked_by_doc, vector_database.collection)
            evaluation_retrieval.evaluation_top_5k(method, chunk_size, overlap)


            

            
            
            

    

