from pypdf import PdfReader

#Let PDF's be uploaded via api and text extracted from pdf
def extract_pdf(file):
    reader = PdfReader(file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80):
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start: start + chunk_size]
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap 
    return chunks
    