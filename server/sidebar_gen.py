import io
from PIL import Image, ImageDraw, ImageFont
from server.state import LLMState

def generate_sidebar_image(state: LLMState) -> bytes:
    # Typical sidebar resolution for Mirabox/AKP153 is around 85x450
    width, height = 85, 450
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("Arial.ttf", 20)
        font_text = ImageFont.truetype("Arial.ttf", 16)
    except IOError:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # Draw Title
    title = state.llm.capitalize()
    draw.text((10, 20), title, fill="white", font=font_title)
    
    # Draw separator
    draw.line((10, 50, width-10, 50), fill="gray", width=2)
    
    # Draw Stats
    y = 70
    stats = [
        f"5H: {state.h5}%",
        f"Week: {state.weekly}%",
        f"Month: {state.monthly}%"
    ]
    
    for stat in stats:
        draw.text((10, y), stat, fill="white", font=font_text)
        y += 40
        
    # Rotate because the physical screen is likely rotated 90 degrees
    img = img.rotate(90, expand=True)

    # Convert to JPEG (Keep quality at 80 to prevent buffer overflow)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=80)
    return buffer.getvalue()
