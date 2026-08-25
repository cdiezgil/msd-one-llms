from fastapi import FastAPI
import uvicorn

from server.state import LLMState, calculate_traffic_light

app = FastAPI()

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
