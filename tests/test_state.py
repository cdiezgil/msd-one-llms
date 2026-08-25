from server.state import calculate_traffic_light, LLMState, TrafficLight

def test_calculate_traffic_light_red():
    state = LLMState(llm="claude", h5=95, weekly=40, monthly=10)
    assert calculate_traffic_light(state) == TrafficLight.RED

def test_calculate_traffic_light_yellow():
    state = LLMState(llm="claude", h5=85, weekly=40, monthly=10)
    assert calculate_traffic_light(state) == TrafficLight.YELLOW

def test_calculate_traffic_light_green():
    state = LLMState(llm="claude", h5=50, weekly=40, monthly=10)
    assert calculate_traffic_light(state) == TrafficLight.GREEN

def test_calculate_traffic_light_gray():
    state = LLMState(llm="claude", h5=-1, weekly=-1, monthly=-1)
    assert calculate_traffic_light(state) == TrafficLight.GRAY
