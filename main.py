from fastapi import FastAPI, File, UploadFile
from pdf_extract_chunking import extract_pdf
from generation import first_message, system_prompt, model, client
from pydantic import BaseModel 


app = FastAPI()

class Questions(BaseModel):
    question: str 

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

# Function that receives prompt( str) 
@app.post("/ask/")
def message(request: Questions): 
    response, response_id =  first_message(client, request.question, system_prompt, model)
    return{"Answer": response}

