from PIL import Image, ImageDraw
from server.state import TrafficLight

def generate_key_image(llm: str, color: str | TrafficLight) -> bytes:
    # Get string representation
    color_str = color.value if isinstance(color, TrafficLight) else color
    
    # Create a 72x72 square (typical macro key size, to be adjusted)
    img = Image.new('RGB', (72, 72), color='black')
    draw = ImageDraw.Draw(img)
    
    # Map color string to RGB
    colors = {"RED": (255, 0, 0), "YELLOW": (255, 255, 0), "GREEN": (0, 255, 0), "GRAY": (128, 128, 128)}
    border_color = colors.get(color_str, (128, 128, 128))
    
    # Draw border
    draw.rectangle([0, 0, 71, 71], outline=border_color, width=4)
    
    # Convert to bytes (raw RGB for now, will compress later if needed)
    return img.tobytes()
