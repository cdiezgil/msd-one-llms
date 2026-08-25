import hid

def scan_devices():
    for device in hid.enumerate():
        # Print all devices to help identify the MSD-ONE VID/PID
        print(f"VID: {device['vendor_id']:04x}, PID: {device['product_id']:04x}, Product: {device['product_string']}")

if __name__ == "__main__":
    scan_devices()
