from main import extract_pdf

with open("algorithms_value_free.pdf","rb") as f:
    text = extract_pdf(f)

print(text)

