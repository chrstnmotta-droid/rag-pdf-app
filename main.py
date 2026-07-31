from fastapi import FastAPI, File, UploadFile
from pdf_utiliz import chunk_text, extract_pdf
app = FastAPI()

@app.get("/hello/{name}") #Placeholder
def hello(name: str):
    return {"message": f"Hello {name}"}

#Connect via api
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {
        "filename": file.filename, 
        "num_chunks": len(chunks),
        "first_chunk": chunks[0] if chunks else "",
        "last_chunk": chunks[-1] if chunks else ""
            }


