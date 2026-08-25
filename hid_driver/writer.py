import hid
import sys

VID = 0x0b00
PID = 0x1000
PACKET_SIZE = 512

def send_image(key_id: int, jpeg_bytes: bytes) -> None:
    device = hid.device()
    try:
        device.open(VID, PID)
    except IOError as e:
        print(f"Warning: Could not connect to HID device {VID:04x}:{PID:04x}: {e}")
        return

    try:
        size = len(jpeg_bytes)
        
        # 16-byte initialization packet
        init_header = [
            0x43, 0x52, 0x54, 0x00, 0x00, 0x42, 0x41, 0x54, 
            0x00, 0x00, (size >> 8) & 0xFF, size & 0xFF, 
            key_id, 0x00, 0x00, 0x00
        ]
        init_packet = bytes(init_header) + b'\x00' * (PACKET_SIZE - len(init_header))
        device.write(init_packet)

        # Chunk and send JPEG data in exactly 512-byte packets
        for i in range(0, size, PACKET_SIZE):
            chunk = jpeg_bytes[i:i+PACKET_SIZE]
            if len(chunk) < PACKET_SIZE:
                chunk += b'\x00' * (PACKET_SIZE - len(chunk))
            device.write(chunk)

        # 16-byte flush packet
        flush_header = [
            0x43, 0x52, 0x54, 0x00, 0x00, 0x53, 0x54, 0x50, 
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        flush_packet = bytes(flush_header) + b'\x00' * (PACKET_SIZE - len(flush_header))
        device.write(flush_packet)

    finally:
        device.close()
