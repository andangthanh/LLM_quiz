from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
import instructor

# Pydantic 
class QuestionAnswers(BaseModel):
    question: str = Field(description="The question")
    possible_answers: List[str] = Field(description="The four possible answers", min_length=4, max_length=4)
    unique_solution: str = Field(description="The unique solution")


client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON
)

user_input = input("Topic: ")
template = f"""
Generate a multiple-choice question with a unique solution and four possible answers with the user's topic {user_input}. 
"""

resp = client.chat.completions.create(
    model="mistral",
    messages=[
        {
            "role": "user",
            "content": template,
        }
    ],
    response_model=QuestionAnswers,
)

print(resp.question)
print(resp.possible_answers)
print(resp.unique_solution)