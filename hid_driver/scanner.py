try:
    import hid
except ImportError:
    print("Warning: 'hid' module not found. Please install it using 'pip install hidapi'.")
    hid = None

def scan_devices():
    if not hid:
        return
    for device in hid.enumerate():
        # Print all devices to help identify the MSD-ONE VID/PID
        print(f"VID: {device['vendor_id']:04x}, PID: {device['product_id']:04x}, Product: {device.get('product_string', 'Unknown')}")

if __name__ == "__main__":
    scan_devices()
