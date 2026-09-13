# - extract_pdf voor alle vier
# - loop voor alle 2 de methodes
#     - binnen loop over overlap en chunking_size (character/sentence )
#     - chunk de text
#     - reset chroma collection
#     - embed + store chunks
#     - run evaluation met method, chunk_size en overlap wordt automatisch opgeslagen (elke run geeft 1 rij)

from vector_database import collection, store_embeddings

#Extract pdfs
extracted_text = {}
for i in ["algorithms_value_free.pdf", "clark_2025.pdf", "Creek_Helman_2022.pdf", "fooling_shap.pdf"]:
    extracted_text[i] = extract_pdf(i)

for method in ["character", "sentence","token"]:
    chunked_by_doc = {}
    for chunk_size in [200, 400, 800, 1200]:
        for overlap_pct in [0, 0.10, 0.20]:
            overlap = chunk_size * overlap
            for pdf, text in extracted_text.items():
                if method == "character":
                    chunked_by_doc[pdf] = character_chunking(text,chunk_size, overlap)
                elif method == "sentence"
                    chunked_by_doc[pdf] = sentence_aware_chunking(text, chunk_size, overlap)
                else:
                    
            
            

    

