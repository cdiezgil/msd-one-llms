import hid
device = hid.device()
try:
    device.open(0x0b00, 0x1000)
    device.set_nonblocking(False)
    print("Opened device")
    res = device.read(64, timeout_ms=50)
    print(f"Read result: {res}")
    device.close()
except Exception as e:
    print(f"Error: {e}")
