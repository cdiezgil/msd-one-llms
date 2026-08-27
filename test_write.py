import hid
import io
import time
from PIL import Image

VID = 0x0b00
PID = 0x1000
PACKET_SIZE = 512

img = Image.new('RGB', (85, 85), color='blue')
buffer = io.BytesIO()
img.save(buffer, format='JPEG', quality=80)
jpeg_bytes = buffer.getvalue()
size = len(jpeg_bytes)

def test(nonblocking):
    device = hid.device()
    device.open(VID, PID)
    device.set_nonblocking(nonblocking)
    
    key_id = 1
    init_header = [
        0x43, 0x52, 0x54, 0x00, 0x00, 0x42, 0x41, 0x54, 
        0x00, 0x00, (size >> 8) & 0xFF, size & 0xFF, 
        key_id, 0x00, 0x00, 0x00
    ]
    init_packet = bytes(init_header) + b'\x00' * (PACKET_SIZE - len(init_header))
    res1 = device.write(init_packet)
    print(f"Nonblocking {nonblocking} write init: {res1}")

    for i in range(0, size, PACKET_SIZE):
        chunk = jpeg_bytes[i:i+PACKET_SIZE]
        if len(chunk) < PACKET_SIZE:
            chunk += b'\x00' * (PACKET_SIZE - len(chunk))
        device.write(chunk)

    flush_header = [
        0x43, 0x52, 0x54, 0x00, 0x00, 0x53, 0x54, 0x50, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    flush_packet = bytes(flush_header) + b'\x00' * (PACKET_SIZE - len(flush_header))
    res2 = device.write(flush_packet)
    print(f"Nonblocking {nonblocking} write flush: {res2}")
    device.close()

try:
    test(True)
except Exception as e:
    print(f"Test True failed: {e}")

try:
    test(False)
except Exception as e:
    print(f"Test False failed: {e}")
