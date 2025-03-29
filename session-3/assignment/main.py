from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import openai
import subprocess
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o")  # Replace with your actual API key

def call_llm(prompt, memory):
    messages = [{"role": "user", "content": m["query"]} for m in memory]
    messages.append({"role": "user", "content": prompt})
    
    response = llm(messages)
    result = response.content
    memory.append({"query": prompt, "response": result})
    return result

app = FastAPI()
memory = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OR ["*"] if for local testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "sk-..."  # Replace with your actual key

class PromptRequest(BaseModel):
    prompt: str

class ShellRequest(BaseModel):
    command: str

@app.post("/agent")
async def agent(request: PromptRequest):
    prompt = request.prompt
    print("prompt GPT", flush=True)
    
    # Prepare messages with history
    messages = [{"role": "user", "content": m["query"]} for m in memory]
    messages.append({"role": "user", "content": prompt})
    
    # # LLM Call
    # response = openai.ChatCompletion.create(
    #     model="gpt-4o",
    #     messages=messages
    # )
    # result = response['choices'][0]['message']['content']
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    memory.append({"query": prompt, "response": result})
    # response = llm(messages)
    # result = response.content
    # memory.append({"query": prompt, "response": result})
    
    print(result, flush=True)
    return JSONResponse(content={"result": result, "memory": memory})

@app.post("/shell")
async def shell(request: ShellRequest):
    command = request.command
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return {"output": result}
    except subprocess.CalledProcessError as e:
        return {"output": e.output}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
