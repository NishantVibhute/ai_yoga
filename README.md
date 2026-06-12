# ai_yoga# AI Yoga Coach

Real-time Yoga Pose Detection and Guidance using OpenCV, MediaPipe, and Python.

## Features

* Real-time webcam pose detection
* Yoga posture analysis
* Skeleton visualization
* Green/Red body part highlighting
* Voice coaching
* Hold timer
* Pose completion detection
* Category-based pose selection
* Reference pose images
* Accuracy scoring
* Scalable architecture for adding new yoga poses

---

## Project Structure

```text
YogaAI/
│
├── assets/
│   ├── tadasana.jpg
│   ├── vrikshasana.jpg
│   └── ...
│
├── core/
│   ├── detector.py
│   ├── renderer.py
│   ├── pose_engine.py
│   ├── voice.py
│   ├── landmarks.py
│   └── angles.py
│
├── poses/
│   ├── pose_registry_standing.py
│   ├── pose_registry_sitting.py
│   ├── pose_registry_prone.py
│   ├── pose_registry_supine.py
│   └── categories.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Create Virtual Environment

### Windows

```bash
py -3.11 -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install opencv-python mediapipe numpy pyttsx3
```

---

## Generate requirements.txt

```bash
pip freeze > requirements.txt
```

---

## Run Application

```bash
python main.py
```

---

## Controls

### Category Menu

```text
1-9 : Select Category
ESC : Exit
```

### Pose Menu

```text
1-9 : Select Pose
B   : Back
ESC : Exit
```

### Info Screen

```text
S : Start Pose Detection
B : Back
ESC : Exit
```

### Detection Screen

```text
B : Back To Info
M : Main Menu
V : Toggle Voice
ESC : Exit
```

---

## Current Poses

### Standing Yoga

* Tadasana
* Vrikshasana
* Padahastasana

### Upcoming

* Ardha Chakrasana
* Trikonasana
* Vajrasana
* Bhadrasana
* Bhujangasana
* Shalabhasana
* Setubandhasana
* Pavanamuktasana
* Ardha Halasana

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* pyttsx3

---

## Future Enhancements

* Multi-language voice coaching
* Session mode
* Progress tracking
* Yoga routine generator
* AI-powered posture recommendations
* Mobile application
* Raspberry Pi Yoga Coach Robot

---

## Author

Nishant Vibhute

AI Yoga Coach is an educational and wellness-focused project that provides real-time yoga posture guidance using computer vision and artificial intelligence.
