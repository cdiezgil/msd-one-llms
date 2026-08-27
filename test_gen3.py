from server.image_gen import generate_key_image
import io
from PIL import Image

def generate_key_image_lowq(llm: str) -> int:
    import os
    img = Image.new('RGB', (85, 85), color='black')
    icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{llm.lower()}.png")
    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize((77, 77), Image.Resampling.LANCZOS)
    img.paste(icon, (4, 4), icon)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=80, subsampling=1)
    return len(buffer.getvalue())

for llm in ['claude', 'gemini', 'kimi', 'z.ai']:
    print(f"{llm} (q=80): {generate_key_image_lowq(llm)} bytes")
