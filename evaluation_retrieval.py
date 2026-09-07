# pseudo_code: Receive golden passages as query -> Retrieve top 5k -> Loop to Check if golden chunk is in top 5k (for multi hop check if all gold chunks in top 5k) amd Check positions for chunks
# in top 5k (skip unanswerable in loop) -> Store whether gold chunk in top 5 k and which position -> record MRR output recall@k -> Store in different file recall@k, MRR, chunk_size, overlap, and embedding model
import retrieval
import json
import os 
import csv
from embeddings import EMBEDDING_MODEL
from pdf_utiliz import DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP


def evaluation_top_5k():
    #Query + expected answer
    with open("golden_set.json") as f:
        golden_set = json.load(f)
    total_answers = len([item for item in golden_set if item["type"] != "unanswerable"])
    total_hits = 0 
    reciprocal_ranks = []
    for item in golden_set:
        if item["type"] == "unanswerable":
            continue
        question = item["question"]
        gold_chunk = item["gold_chunk"]
        # Retrieval top 5k
        top_k = retrieval.retrieval_top_5k(question)
        retrieved_chunks = top_k["documents"][0]
        hits = 0 
        rank = 0
        positions = []
        # Check position and presence of golden_chunk 
        if item["type"] == "single_hop":
            for i,v in enumerate(retrieved_chunks):
                if gold_chunk in v:
                    total_hits += 1 
                    rank = i + 1
                    reciprocal_ranks.append(1 / rank)
                    break
                else:
                    continue
        # Check positions and presence of ALL golden_chunks
        elif item["type"] == "multi_hop":
            # checks whether particular chunk is already found in top 5k
            c_found = []
            for i,v in enumerate(retrieved_chunks):
                for c in gold_chunk:
                    if c in v and c not in c_found:
                        hits += 1
                        rank = i + 1
                        positions.append(rank)
                        c_found.append(c)
                        continue
                    else:
                        continue
            if hits == len(gold_chunk):
                total_hits += 1
                if len(positions) > 0:
                    reciprocal_ranks.append(1 / (sum(positions)/ len(positions)))

    recall_at_k = total_hits / total_answers 
    if len(reciprocal_ranks) > 0:
        mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) 
    else:
        mrr = 0
    
    file_exists = os.path.exists("results.csv")
    with open("results.csv", mode ="a", newline= "") as f:
        if not file_exists:
            csv.writer(f).writerow(["Embedding", "Chunk size", "Overlap", "Mrr", "Recall@K"])
        csv.writer(f).writerow([EMBEDDING_MODEL, DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP, mrr, recall_at_k])

