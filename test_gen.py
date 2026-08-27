from server.image_gen import generate_key_image
from server.state import TrafficLight

for llm in ['claude', 'gemini', 'kimi', 'z.ai']:
    data = generate_key_image(llm, TrafficLight.GREEN)
    print(f"{llm}: {len(data)} bytes")
