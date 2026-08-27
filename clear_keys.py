import io
from PIL import Image
from hid_driver.hid_manager import hid_manager

def clear():
    img = Image.new('RGB', (85, 85), color='black')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=80)
    jpeg_bytes = buffer.getvalue()
    
    for k in range(1, 16):
        if k not in [4, 7, 10, 13]: # Keep our LLMs
            hid_manager.send_image(k, jpeg_bytes)
            
clear()
