from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from pypdf import PdfReader

app = FastAPI()

@app.get("/hello/{name}") #Placeholder
def hello(name: str):
    return {"message": f"Hello {name}"}

#Let PDF's be uploaded via api and text extracted from pdf
def extract_pdf(file_object):
    reader = PdfReader(file_object)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80):
    chunks = []
    start = 0
    while start < len(text):
        chunk =text[start: start + chunk_size]
        if chunk:
            chunks.append()
        start += chunk_size - overlap 
    return chunks

#Connect via api
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    text = extract_pdf(file.file)
    chunks = chunk_text(text)
    return {
        "filename": file.filename, 
        "num_chunks": len(chunks),
        "first_chunk": chunks[0] if chunks else "",
        "last_chunk": chunks[-1] if chunks else ""
            }


