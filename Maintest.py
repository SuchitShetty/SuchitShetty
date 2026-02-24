from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Hello Suchit 🚀 This message is from FastAPI!</h1>"

@app.get("/message")
def message():
    return {"message": "This is a JSON response from FastAPI"}