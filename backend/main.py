from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = FastAPI()

# Initialize model
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

class TopicRequest(BaseModel):
    topic: str

@app.post("/generate_question/")
async def generate_question(request: TopicRequest):
    prompt = f"Generate a multiple-choice question about {request.topic} with four answers."
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    question = generated_text.split("\n")[0]
    answers = generated_text.split("\n")[1:]
    return {"question": question, "answers": answers}
