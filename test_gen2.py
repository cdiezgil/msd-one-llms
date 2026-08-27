import io
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (85, 85), color='black')
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, 84, 84], outline=(255,0,0), width=4)
font = ImageFont.load_default()
draw.text((30, 30), "C", fill="white", font=font)
buffer = io.BytesIO()
img.save(buffer, format='JPEG', quality=95, subsampling=0)
print(f"Single letter: {len(buffer.getvalue())} bytes")
