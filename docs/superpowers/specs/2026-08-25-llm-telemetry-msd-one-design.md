# Design Spec: LLM Telemetry Dashboard for Mars Gaming MSD-ONE

## Overview
A local telemetry system to monitor usage limits for four LLM subscriptions (Gemini, Claude, Z.ai, Kimi). The system extracts real-time consumption data from the user's browser and displays it on the LCD keys and side screen of a Mars Gaming MSD-ONE macro keyboard, bypassing the proprietary software via USB HID reverse engineering.

## Architecture

The system consists of three isolated components:

### 1. Browser Extension (Data Extractor)
- **Environment**: Chrome/Edge Extension (Manifest V3).
- **Responsibilities**: 
  - Inject content scripts into the domains of Gemini, Claude, Z.ai, and Kimi.
  - Monitor DOM changes and intercept XHR/Fetch network requests to detect limit status.
  - Extract detailed metrics: 5-hour, weekly, and monthly limit percentages.
  - Send JSON payloads via HTTP POST to the Local Server when states change.
- **Error Handling**: If a DOM changes and data cannot be parsed, send an "unknown" state to the server rather than crashing.

### 2. Local Python Server (Telemetry Backend)
- **Environment**: Python 3.x (FastAPI or Flask).
- **Responsibilities**:
  - Run an HTTP server on a local port (e.g., `localhost:5000`) to receive extension payloads.
  - Calculate global "Traffic Light" states (Green = safe, Yellow = warning, Red = limit reached, Gray = unknown) based on the received percentages.
  - Use `Pillow` to dynamically generate UI images:
    - **Keys (x4)**: Small square images with the LLM logo and a colored border (Traffic Light state).
    - **Sidebar**: A large rectangular image containing text/progress bars for the 5h, weekly, and monthly metrics.
- **Error Handling**: Maintain the last known state in memory. Re-attempt USB connections if the keyboard is disconnected.

### 3. USB HID Controller (Hardware Layer)
- **Environment**: Python (`hidapi` or `pyusb`).
- **Responsibilities**:
  - **Read**: Listen for interrupt transfers from the MSD-ONE to detect when one of the 4 LLM keys is pressed.
  - **Write**: Send raw hexadecimal payloads to update the LCD keys and the Sidebar screen.
- **Integration**: Runs as a background thread within the Python Server. When a key press event is detected (e.g., "Key 1 pressed"), the controller asks the Server for the specific LLM Sidebar Image and sends it to the Sidebar screen endpoint.

## Phase 1: USB Forensic Plan (Prerequisite)
Since there is no official API, implementation MUST begin with reverse engineering:
1. Capture USB traffic using Wireshark + USBPcap while running the official Mars Gaming software.
2. Identify VID/PID.
3. Isolate the payload structure for:
   - Setting a single key image (Header + Payload size + Image format).
   - Setting the sidebar image.
   - Key press event codes.

## Open Considerations
- **LLM DOM Volatility**: The web interfaces for these LLMs change frequently. The extension's scraping logic will need to be modular and easy to update.
- **Image Formats**: The MSD-ONE might require a specific image format (e.g., BMP, RGB565 raw pixels, or JPEG) which will dictate how `Pillow` encodes the output byte streams.
