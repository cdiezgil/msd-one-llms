import hid
import threading
import time

VID = 0x0b00
PID = 0x1000
PACKET_SIZE = 512

class HIDManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(HIDManager, cls).__new__(cls)
                cls._instance._init()
            return cls._instance

    def _init(self):
        self.device = hid.device()
        self.connected = False
        self.read_thread = None
        self.on_click_callback = None
        self.write_lock = threading.Lock()
        
        try:
            self.device.open(VID, PID)
            self.device.set_nonblocking(False)  # MUST be blocking for reliable writes!
            self.connected = True
            print(f"[HID] Connected to device {VID:04x}:{PID:04x}")
            
            # Start background reader thread
            self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self.read_thread.start()
        except IOError as e:
            print(f"[HID] Warning: Could not connect to device: {e}")

    def _read_loop(self):
        while self.connected:
            try:
                # Serialize USB access: don't read exactly while writing
                with self.write_lock:
                    report = self.device.read(64, timeout_ms=50)
                    
                if report and len(report) >= 10:
                    # report[9] is the key ID
                    if report[0] == 0x41 and report[1] == 0x43 and report[2] == 0x4b:
                        key_id = report[9]
                        if self.on_click_callback:
                            # Run in a separate thread so we don't block the read loop
                            threading.Thread(target=self.on_click_callback, args=(key_id,), daemon=True).start()
            except Exception as e:
                print(f"[HID] Read error: {e}")
                time.sleep(1)

    def set_callback(self, callback):
        self.on_click_callback = callback

    def send_image(self, key_id: int, jpeg_bytes: bytes) -> None:
        if not self.connected:
            return
            
        with self.write_lock:
            try:
                size = len(jpeg_bytes)
                
                init_header = [
                    0x43, 0x52, 0x54, 0x00, 0x00, 0x42, 0x41, 0x54, 
                    0x00, 0x00, (size >> 8) & 0xFF, size & 0xFF, 
                    key_id, 0x00, 0x00, 0x00
                ]
                init_packet = bytes(init_header) + b'\x00' * (PACKET_SIZE - len(init_header))
                self.device.write(init_packet)

                for i in range(0, size, PACKET_SIZE):
                    chunk = jpeg_bytes[i:i+PACKET_SIZE]
                    if len(chunk) < PACKET_SIZE:
                        chunk += b'\x00' * (PACKET_SIZE - len(chunk))
                    self.device.write(chunk)

                flush_header = [
                    0x43, 0x52, 0x54, 0x00, 0x00, 0x53, 0x54, 0x50, 
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                ]
                flush_packet = bytes(flush_header) + b'\x00' * (PACKET_SIZE - len(flush_header))
                self.device.write(flush_packet)
            except Exception as e:
                print(f"[HID] Write error: {e}")

hid_manager = HIDManager()
