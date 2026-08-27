import io
import time
from PIL import Image, ImageDraw, ImageFont
from hid_driver.hid_manager import hid_manager

def send_test_image(k):
    img = Image.new('RGB', (85, 450), color='blue')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), f"ID {k}", fill="white")
    img = img.rotate(90, expand=True)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=80)
    hid_manager.send_image(k, buffer.getvalue())
    print(f"Sent to ID {k}")

# Send to 0 and 16 to 20
for k in [0, 16, 17, 18, 19, 20]:
    send_test_image(k)
    time.sleep(1)
