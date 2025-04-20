# 🎓 Student Attention Analyser

A smart classroom tool for analyzing student engagement through facial attendance logging and hand-raise detection using computer vision and deep learning.

---

## 🧠 Overview

**Student Attention Analyser** is a two-part system designed to help educators measure student engagement during a session:

1. **Face-Based Attendance Logging**  
   Uses facial recognition to log student attendance in real time.

2. **Hand-Raise Detection & Attention Tracking**  
   Detects and logs hand-raising activity using a pretrained YOLOv5 model. This data is used to assess attentiveness, participation, and engagement.

---

## 📂 Project Structure

student_attention_analyser/ <br>
├── yolov5/ # YOLOv5 cloned repository <br>
├── dataset/ # Label definitions for hand raise detection <br>
├── evaluation/ #contains evaluation of model and some extra files used for image pre-processing and manipulation<br>
├── hand_raise_detector_valid/ #trained yolov5 instance<br>
├── ImagesAttendance/ #student image dataset for attendance <br>
├── attendance_log.csv/<br>
├── hand_raise_log.csv/<br>
├── test.py # Script for testing model accuracy or demoing <br>
├── student_detection.py # Main application for face detection + attendance <br>
├── tracker.py # Analyzes hand raises and generates insight reports <br>
├── requirements.txt # Required Python packages <br>
└── README.md<br>

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/student_attention_analyser.git
cd student_attention_analyser
```

### 2. Set Up the Environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

### 3. Clone YOLOv5
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
cd ..

---

## ▶️ Usage
### Test the model
python test.py
### Run face detection for attendance
python student_detection.py
### Analyze hand-raise activity and generate visualizations
python tracker.py
---

## 🧠 Model Details
YOLOv5 Pretrained Model
Used for detecting hand raises (hand_up, hand_down).

Face Detection
Built with OpenCV + Dlib or a face recognition model (depending on implementation).

## 📊 Output
Attendance logs with timestamps and recognized student faces.

Event logs containing hand raise frequency per student.

Charts & Stats visualizing engagement and participation.

## 📝 TODO / Coming Soon
Add real-time dashboard (e.g., with Streamlit or Flask).

Improve recognition with class rosters or student photo datasets.

Extend to detect distractions or inattention.

## 📜 License
This project is open-source and available under the MIT License.

## 🙌 Acknowledgements
Ultralytics YOLOv5

OpenCV, NumPy, Matplotlib

