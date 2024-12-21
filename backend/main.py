from fastapi import FastAPI
from pydantic import BaseModel
import torch
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

app = FastAPI()

template = """
Generate a multiple-choice question with a unique solution and four answers with the user's topic {topic}. The formatting of the output should be as following: 

<question_string>
[<answer_string1>, <answer_string2>, <answer_string3>, <answer_string4>]

<question_string>, <answer_string1>, <answer_string2>, <answer_string3>, <answer_string4> should be strings.
No empty line between question and answers.
"""

model = OllamaLLM(model="llama3.2")

class TopicRequest(BaseModel):
    topic: str

@app.post("/generate_question/")
async def generate_question(request: TopicRequest):
    prompt = PromptTemplate.from_template(template)
    chain = prompt | model

    result = chain.invoke({"topic": {request.topic}})
    question = generated_text.split("\n")[0]
    answers = generated_text.split("\n")[1:]
    return {"question": question, "answers": answers}
