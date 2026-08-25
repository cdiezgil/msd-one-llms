import sys
import os

# Dynamically insert the parent directory into sys.path before imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from server.state import LLMState, calculate_traffic_light

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_states = {}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/update")
def update_state(state: LLMState):
    llm_states[state.llm] = state
    light = calculate_traffic_light(state)
    return {"status": "updated", "light": light}

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=5000, reload=True)
