from pypdf import PdfReader
from nltk.tokenize import sent_tokenize
import tiktoken 

#Let PDF's be uploaded via api and text extracted from pdf
def extract_pdf(file):
    reader = PdfReader(file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

# Character_based chunking 
def character_chunking(text: str, overlap: int, chunk_size: int):
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
    sentences = nltk.tokenize.sent_tokenize(text, language = "english")
    current_chunk = ""
    overlapping_text = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            overlapping_text = current_chunk[-overlap:]
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




