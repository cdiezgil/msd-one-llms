import io
from PIL import Image, ImageDraw
from server.state import TrafficLight

def generate_key_image(llm: str, color: str | TrafficLight) -> bytes:
    # TODO: draw LLM text on image (using the 'llm' argument)
    
    # Get string representation
    color_str = color.value if isinstance(color, TrafficLight) else color
    color_str = color_str.upper()
    
    # Create a 96x96 square (true MSD-ONE size)
    img = Image.new('RGB', (96, 96), color='#0A1122')
    draw = ImageDraw.Draw(img)
    
    # Map color string to RGB
    colors = {"RED": (255, 0, 0), "YELLOW": (255, 255, 0), "GREEN": (0, 255, 0), "GRAY": (128, 128, 128)}
    border_color = colors.get(color_str, (128, 128, 128))
    
    import os

    # Convert LLM string to a single uppercase letter fallback
    display_text = llm[0].upper() if llm else "?"

    # Draw border (we draw it at the end to ensure it sits on top)
    # First, let's try to load the icon
    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{llm.lower()}.png")
    icon_loaded = False
    
    if os.path.exists(icon_path):
        try:
            icon = Image.open(icon_path).convert("RGBA")
            # Resize icon to fit inside the border (96-12=84 pixels roughly)
            icon = icon.resize((84, 84), Image.Resampling.LANCZOS)
            # Paste the icon into the center (6, 6)
            img.paste(icon, (6, 6), icon)
            icon_loaded = True
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
            
    if not icon_loaded:
        # Use a HUGE font for the single letter fallback
        from PIL import ImageFont
        try:
            font = ImageFont.truetype("Arial.ttf", 54)
        except IOError:
            try:
                font = ImageFont.truetype("Helvetica.ttc", 54)
            except IOError:
                font = ImageFont.load_default()

        # Draw text in the center
        text_bbox = draw.textbbox((0, 0), display_text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        text_x = (96 - text_w) / 2
        text_y = (96 - text_h) / 2 - 4
        draw.text((text_x, text_y), display_text, fill="white", font=font)

    # Finally, draw the colored border over the edges to frame it (thicker)
    draw.rectangle([0, 0, 95, 95], outline=border_color, width=8)
    
    # Hardware requires the image to be rotated 90 degrees left
    img = img.rotate(90)

    # Convert to JPEG bytes
    # IMPORTANT: Keep quality at 80 to prevent the JPEG from exceeding ~4KB. 
    # The MSD-ONE firmware buffer overflows and crashes if the image is too large!
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=80)
    return buffer.getvalue()
