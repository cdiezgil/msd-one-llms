import io
from PIL import Image, ImageDraw, ImageFont

def generate_stat_tile(title: str, text: str, color: str = "BLUE") -> bytes:
    img = Image.new('RGB', (96, 96), color='#0A1122')
    draw = ImageDraw.Draw(img)
    
    # Map color string to RGB
    colors = {"RED": (255, 0, 0), "YELLOW": (255, 255, 0), "GREEN": (0, 255, 0), "BLUE": (0, 128, 255)}
    border_color = colors.get(color, (0, 128, 255))
    
    draw.rectangle([0, 0, 95, 95], outline=border_color, width=4)
    
    try:
        font_title = ImageFont.truetype("Arial.ttf", 20)
        font_value = ImageFont.truetype("Arial.ttf", 16) # Smaller font to fit both stats
    except IOError:
        font_title = ImageFont.load_default()
        font_value = ImageFont.load_default()

    # Draw Title (e.g. "CLAU")
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((96 - title_w) / 2, 8), title, fill="white", font=font_title)
    
    # Draw Stats Lines (split by space)
    lines = text.split(" ")
    y = 32
    for line in lines:
        val_bbox = draw.textbbox((0, 0), line, font=font_value)
        val_w = val_bbox[2] - val_bbox[0]
        draw.text(((96 - val_w) / 2, y), line, fill=border_color, font=font_value)
        y += 20
    
    img = img.rotate(90)
    
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=80)
    return buffer.getvalue()
