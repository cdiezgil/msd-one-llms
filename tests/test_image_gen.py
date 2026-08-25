import io
from PIL import Image
from server.image_gen import generate_key_image
from server.state import TrafficLight

def test_generate_key_image_returns_bytes():
    img_bytes = generate_key_image("claude", "RED")
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 0
    # Check JPEG header
    assert img_bytes.startswith(b'\xff\xd8\xff')
    
    # Check size
    img = Image.open(io.BytesIO(img_bytes))
    assert img.size == (85, 85)

def test_generate_key_image_with_enum():
    img_bytes = generate_key_image("claude", TrafficLight.RED)
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 0
    # Check JPEG header
    assert img_bytes.startswith(b'\xff\xd8\xff')
    
    # Check size
    img = Image.open(io.BytesIO(img_bytes))
    assert img.size == (85, 85)
