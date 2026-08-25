import io
from PIL import Image, ImageDraw
from server.state import TrafficLight

def generate_key_image(llm: str, color: str | TrafficLight) -> bytes:
    # TODO: draw LLM text on image (using the 'llm' argument)
    
    # Get string representation
    color_str = color.value if isinstance(color, TrafficLight) else color
    color_str = color_str.upper()
    
    # Create an 85x85 square (MSD-ONE typical size)
    img = Image.new('RGB', (85, 85), color='black')
    draw = ImageDraw.Draw(img)
    
    # Map color string to RGB
    colors = {"RED": (255, 0, 0), "YELLOW": (255, 255, 0), "GREEN": (0, 255, 0), "GRAY": (128, 128, 128)}
    border_color = colors.get(color_str, (128, 128, 128))
    
    # Draw border
    draw.rectangle([0, 0, 84, 84], outline=border_color, width=4)
    
    # Convert to JPEG bytes
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=95, subsampling=0)
    return buffer.getvalue()
