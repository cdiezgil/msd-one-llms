import hid
import time

VID = 0x0b00
PID = 0x1000

def listen_for_clicks():
    device = hid.device()
    try:
        device.open(VID, PID)
        device.set_nonblocking(False) # Block until a key is pressed
        print(f"Listening for button presses on {VID:04x}:{PID:04x}...", flush=True)
        
        while True:
            # The device usually sends a small report when a key is pressed or released
            report = device.read(64)
            if report:
                hex_report = [hex(b) for b in report]
                print(f"Received HID input: {hex_report}", flush=True)
    except IOError as e:
        print(f"Error: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    listen_for_clicks()
