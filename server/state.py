from pydantic import BaseModel

class LLMState(BaseModel):
    llm: str
    h5: float
    weekly: float
    monthly: float

def calculate_traffic_light(state: LLMState) -> str:
    # Thresholds: > 90% is RED, > 80% is YELLOW, else GREEN
    max_usage = max(state.h5, state.weekly, state.monthly)
    if max_usage >= 90:
        return "RED"
    elif max_usage >= 80:
        return "YELLOW"
    return "GREEN"
