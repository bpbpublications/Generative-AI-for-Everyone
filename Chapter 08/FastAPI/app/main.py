from transformers import pipeline
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")

app = FastAPI()

class Item(BaseModel):
    text: str

@app.get('/')
def root():
  return HTMLResponse(content='<h1>A Self-documenting API for content summaraization</h1>', status_code=200)

@app.post('/summarize')
def summarize(item: Item):
  return summarizer(item.text, min_length=5, max_length=30)