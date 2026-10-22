from pypdf import PdfReader
from nltk.tokenize import sent_tokenize
import tiktoken 
import re

def normalize_text(text):
    text = " ".join(text.split())
    text = re.sub(r"\s*∼\s*", "∼", text)
    text = re.sub(r"([a-z])- ([a-z])", r"\1\2", text)  
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl") 
    return text

#Let PDF's be uploaded via api and text extracted from pdf
def extract_pdf(file):
    reader = PdfReader(file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    pdf_text = normalize_text(pdf_text)
    return pdf_text

# Character_based chunking 
def character_chunking(text: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start: start + chunk_size]
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap 
    return chunks

#Sentence_aware chunking
def sentence_aware_chunking(text: str, chunk_size: int, overlap: int):
    chunks = []
    sentences = sent_tokenize(text, language = "english")
    current_chunk = ""
    overlapping_text = ""
    for sentence in sentences:
        if len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            for i in range(0, len(sentence), chunk_size):
                chunks.append(sentence[i: i + chunk_size])
            continue 
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            overlapping_text = current_chunk[-overlap:] if overlap>0 else ""
            current_chunk = ""
            current_chunk = overlapping_text.strip() + " " + sentence + " " 
    if len(current_chunk) > 0:
        chunks.append(current_chunk.strip())
    return chunks

#token_aware chunking
def token_aware_chunking(text: str, chunk_size: int, overlap: int):
    # tekst -> tokens -> text
    enc = tiktoken.encoding_for_model("text-embedding-3-small")
    tokens = enc.encode(text)
    chunks = [] 
    start = 0
    while start < len(tokens):
        chunk_tokens = tokens[start: start + chunk_size]
        if chunk_tokens:
            chunks.append(enc.decode(chunk_tokens))
        start += chunk_size - overlap 
    return chunks




