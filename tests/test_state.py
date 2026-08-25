from server.state import calculate_traffic_light, LLMState

def test_calculate_traffic_light_red():
    state = LLMState(llm="claude", h5=95, weekly=40, monthly=10)
    assert calculate_traffic_light(state) == "RED"

def test_calculate_traffic_light_yellow():
    state = LLMState(llm="claude", h5=85, weekly=40, monthly=10)
    assert calculate_traffic_light(state) == "YELLOW"

def test_calculate_traffic_light_green():
    state = LLMState(llm="claude", h5=50, weekly=40, monthly=10)
    assert calculate_traffic_light(state) == "GREEN"
