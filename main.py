from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}") #Placeholder
def hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/hello/add/{a}/{b}")
def add(a: int, b:int):
    sum = a + b
    return {"result sum": sum}
