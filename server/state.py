from enum import Enum
from pydantic import BaseModel

class TrafficLight(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"
    GRAY = "GRAY"

class LLMState(BaseModel):
    llm: str
    h5: float
    weekly: float
    monthly: float

def calculate_traffic_light(state: LLMState) -> TrafficLight:
    max_usage = max(state.h5, state.weekly, state.monthly)
    # If all values are 0 or below, we can consider it GRAY or just less than 0. Let's say < 0 is GRAY.
    if max_usage < 0:
        return TrafficLight.GRAY
    if max_usage >= 90:
        return TrafficLight.RED
    elif max_usage >= 80:
        return TrafficLight.YELLOW
    return TrafficLight.GREEN
