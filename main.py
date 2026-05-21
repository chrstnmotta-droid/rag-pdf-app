from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from pypdf import PdfReader
import json

app = FastAPI()

@app.get("/hello/{name}") #Placeholder
def hello(name: str):
    return {"message": f"Hello {name}"}

#Doel Een pdf kunnen opsturen naar API (software) en tekst extracteren 

# Pseudocode
# 1. Ontvang PDF op POST (data receiver for API) done
# 2. UploadFile om de files daadwerkelijk te uploaden naar api 
# 3. Specifieer type data (tekst)
# 4. Open pdf 
# 5. Parse pdf 
# 6. Loop door de paginas
# 7. Extract de tekst 
# 8. Convert extracted to JSON

def extract_pdf(file_object):
    reader = PdfReader(file_object)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text
   
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    text = extract_pdf(file.file)
    return {"filename": file.filename, "text": text}
