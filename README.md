// ...existing code...
# Interactive Fluid-Background

Interactive visual background driven by hand gestures. Webcam-based hand positions (MediaPipe + OpenCV) are mapped to cursor using PyAutoGUI and injected into a TouchDesigner fluid network to produce colorful, low-latency visual effects.

---

## Quick summary
- Real-time hand tracking (MediaPipe) from webcam frames (OpenCV).  
- Selected hand landmark(s) mapped to input to perturb a fluid field in TouchDesigner.  
- Configurable sensitivity, smoothing and intentional-movement detection to avoid accidental triggers.

---

## Features
- Continuous hand landmark detection (MediaPipe Hands).  
- Cursor mapping & control via PyAutoGUI (or send positions via OSC/UDP).  
- Movement filtering: smoothing, deadzones and velocity thresholds.  
- Low-latency pipeline suitable for live visuals and performance.

---

## Requirements
- Python 3.8+  
- opencv-python  
- mediapipe  
- pyautogui  
- (Optional) numpy, scipy — for improved smoothing/filtering  
- TouchDesigner (099 / 2021+ recommended) — any build that accepts mouse/OSC input  
- Webcam

---

## Configuration & Tuning
- Sensitivity: scales normalized landmark movement to screen coordinates.  
- Smoothing window: exponential or moving average to reduce jitter.  
- Intentional movement threshold: minimum velocity/dispacement before injecting into the fluid.  
- Landmark selection: index fingertip, palm center or averaged point depending on desired interaction.

---

## License & Credits
- Built for experimentation with MediaPipe, OpenCV, PyAutoGUI and TouchDesigner.  
- Credits: MediaPipe for hand detection and TouchDesigner for the fluid network.

