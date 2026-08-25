import sys
import os

# Dynamically insert the parent directory into sys.path before imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from server.state import LLMState, calculate_traffic_light
from server.image_gen import generate_key_image
from hid_driver.hid_manager import hid_manager

app = FastAPI()

from server.expand_gen import generate_stat_tile
import threading
import time
import subprocess

URL_MAP = {
    "claude": "https://claude.ai/new#settings/usage",
    "kimi": "https://www.kimi.ai/membership/subscription?tab=quota",
    "z.ai": "https://z.ai/manage-apikey/coding-plan/personal/usage",
    "gemini": "https://gemini.google.com/"
}

DASHBOARD_KEY = 15

# Double click tracking
last_click_time = {}
click_timer = {}

def execute_single_click(llm_name):
    print(f"🌍 Abriendo navegador para {llm_name.upper()}")
    url = URL_MAP.get(llm_name)
    if url:
        subprocess.run(["open", url])

def execute_double_click(llm_name, state):
    print(f"📊 Dibujando Dashboard en tecla {DASHBOARD_KEY} para {llm_name.upper()}")
    # Generate a single tile with both stats
    tile_bytes = generate_stat_tile(llm_name[:4].upper(), f"5H:{state.h5}% W:{state.weekly}% M:{state.monthly}%", "BLUE")
    try:
        hid_manager.send_image(DASHBOARD_KEY, tile_bytes)
    except Exception as e:
        print(f"❌ Error al dibujar dashboard: {e}")

APP_KEY_MAP = {14: "Claude", 11: "Gemini", 8: "Antigravity", 5: "Ghostty"}

@app.on_event("startup")
def startup_event():
    # Draw app icons on startup
    import os
    from PIL import Image
    import io
    for key_id, app_name in APP_KEY_MAP.items():
        icon_path = os.path.join("icons_apps", f"{app_name}.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).convert("RGB")
            img = img.rotate(90)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=80)
            try:
                hid_manager.send_image(key_id, buffer.getvalue())
            except:
                pass

# Register click callback
def on_key_clicked(key_id: int):
    # Check if it's an app launcher key
    if key_id in APP_KEY_MAP:
        app_name = APP_KEY_MAP[key_id]
        print(f"🚀 Lanzando app: {app_name} (Tecla {key_id})")
        if app_name == "Ghostty":
            subprocess.Popen(["/Applications/Ghostty.app/Contents/MacOS/ghostty", "-e", "ssh cdiezgil@192.168.178.63"])
        else:
            subprocess.run(["open", "-a", app_name])
        return

    # Check if it's an LLM key
    llm_name = next((name for name, k_id in KEY_MAP.items() if k_id == key_id), None)
    if llm_name:
        current_time = time.time()
        prev_time = last_click_time.get(llm_name, 0)
        
        # If it's a double click (less than 400ms)
        if current_time - prev_time < 0.4:
            # Cancel the pending single click timer
            if llm_name in click_timer:
                click_timer[llm_name].cancel()
            
            # Reset time to avoid triple clicks
            last_click_time[llm_name] = 0
            
            # Execute Double Click
            state = llm_states.get(llm_name)
            if state:
                execute_double_click(llm_name, state)
        else:
            # Wait 400ms to see if it becomes a double click
            last_click_time[llm_name] = current_time
            timer = threading.Timer(0.4, execute_single_click, args=(llm_name,))
            click_timer[llm_name] = timer
            timer.start()

hid_manager.set_callback(on_key_clicked)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KEY_MAP = {"claude": 13, "kimi": 10, "z.ai": 7, "gemini": 4}
llm_states = {}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/update")
def update_state(state: LLMState):
    llm_states[state.llm] = state
    light = calculate_traffic_light(state)
    
    jpeg_bytes = generate_key_image(state.llm, light)
    key_id = KEY_MAP.get(state.llm, 13)
    try:
        hid_manager.send_image(key_id, jpeg_bytes)
    except Exception as e:
        print(f"Error sending image to HID: {e}")
    
    return {"status": "updated", "light": light}

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=5001)
