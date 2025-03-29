# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from agent_runner import run_agentic_query
# import uvicorn

# app = FastAPI()

# # Enable CORS for Chrome extension
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# class QueryInput(BaseModel):
#     query: str



# @app.post("/run")
# async def run_agent(query_input: QueryInput):
#     result, logs = run_agentic_query(query_input.query)
#     return {"result": result}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_runner import run_agentic_query
import uvicorn

app = FastAPI()

# Enable CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryInput(BaseModel):
    query: str
    session_id: str = "default"

# Store memory per session
from langchain.memory import ConversationBufferMemory

# Dictionary to track multiple conversations
session_memory = {}

@app.post("/run")
async def run_agent(query_input: QueryInput):
    session_id = query_input.session_id

    # Create memory for session if it doesn't exist
    if session_id not in session_memory:
        session_memory[session_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    result, logs = run_agentic_query(query_input.query, session_memory[session_id])
    return {"result": result, "logs": logs}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)