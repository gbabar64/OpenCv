Interactive Fluid-Background
What is this
An interactive visual background that disturbs a fluid simulation by tracking intentional hand movements. Hand positions are detected with MediaPipe + OpenCV, converted into cursor coordinates with PyAutoGUI and injected into a TouchDesigner fluid setup to create colorful, low-latency, real-time visual effects.
This project was built as an experiment in gestural interaction and live visuals, the hand motion becomes a natural controller that creates ripples, splashes and color shifts in a fluid field.
________________________________________
Features
•	Real-time hand tracking using MediaPipe (hand landmarks) and OpenCV (camera capture).
•	Mapping of selected hand coordinates to cursor positions with PyAutoGUI.
•	Integration with TouchDesigner to perturb a fluid simulation where the point interacts with the fluid field.
•	Configurable sensitivity, smoothing and intentionally-movement detection to avoid accidental triggers.
________________________________________
How it works (high level)
1.	Webcam frames → OpenCV.
2.	MediaPipe extracts hand landmarks (keypoints).
3.	A decision layer filters out small/unintentional motion and selects the control point
4.	PyAutoGUI maps normalized landmark coordinates → cursor coordinates.
5.	TouchDesigner reads the cursor position and uses it to move the fluid.
6.	Visuals react in real time; performance optimizations keep latency low.
________________________________________
Requirements / Dependencies
•	Python 3.8+
•	OpenCV (opencv-python)
•	MediaPipe (mediapipe)
•	PyAutoGUI (pyautogui)
•	(Optional) numpy, scipy for smoothing/filtering
•	TouchDesigner (099 or 2021+ recommended — any version that supports input from mouse or OSC/UDP)
•	A webcam
