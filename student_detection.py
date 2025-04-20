import torch
import cv2
import os
import csv
from datetime import datetime
import face_recognition
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression
from yolov5.utils.torch_utils import select_device

# YOLOv5 Hand Raise Detector Setup
device = select_device('cpu')  # 0-gpu, 'cpu'-cpu
model = DetectMultiBackend('hand_raise_detector_valid/weights/best.pt', device=device)
model.eval()

# Camera setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access the camera")
    exit()

# Setting up database and other run time handlers
image_path = 'ImagesAttendance'  
attendance_log_file = "attendance_log.csv"
hand_raise_log_file = "hand_raise_log.csv"
student_images = []
student_names = []
encode_list_known = []

def load_student_images():
    global encode_list_known, student_names, student_images
    for student_image in os.listdir(image_path):
        image_path_full = os.path.join(image_path, student_image)
        img = cv2.imread(image_path_full)
        student_images.append(img)
        student_names.append(os.path.splitext(student_image)[0])  # Store name without extension

        # Encode student's face
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img_rgb)[0]
        encode_list_known.append(encode)

load_student_images()

def initialize_logs():
    if not os.path.exists(attendance_log_file):
        with open(attendance_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Student", "Date", "Attendance Time"])

    if not os.path.exists(hand_raise_log_file):
        with open(hand_raise_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Student", "Date", "Hand Raise Time"])

initialize_logs()

# Dictionary to track attendance within the current hour
attendance_tracker = {}

def mark_attendance(student_name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H")
    time_str = now.strftime("%H:%M:%S")

    # Check if the student is already marked present for the current hour
    if attendance_tracker.get(student_name) == hour:
        print(f"Attendance for {student_name} already marked for this hour.")
        return

    # Mark attendance
    with open(attendance_log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([student_name, date_str, time_str])
    attendance_tracker[student_name] = hour  # Update tracker
    print(f"Attendance marked for {student_name} at {time_str}")

def log_hand_raise(student_name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    with open(hand_raise_log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([student_name, date_str, time_str])
    print(f"Hand raise logged for {student_name} at {time_str}")

def recognize_student(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encode_list_known, face_encoding)
        face_distances = face_recognition.face_distance(encode_list_known, face_encoding)

        match_index = None
        if len(face_distances) > 0:
            match_index = face_distances.argmin()

        if match_index is not None and matches[match_index]:
            name = student_names[match_index]
            print(f"Student {name} recognized")
            return name, face_location
    return None, None

# Main loop for detection
print("Hand raise detection and attendance system started...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Face recognition
    student_name, face_location = recognize_student(frame)
    if student_name:
        mark_attendance(student_name)

    # Hand raise detection
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    img = img.to(device)

    pred = model(img)
    pred = non_max_suppression(pred, 0.25, 0.45)  # confidence threshold: 0.25, IoU threshold: 0.45

    for det in pred:
        if det is not None and len(det):
            for *xyxy, conf, cls in det:
                if conf > 0.5:  # Only draw boxes with confidence > 0.5
                    label = f"Hand Raise: {conf:.2f}"
                    cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Log hand raise for recognized student
                    if student_name:
                        log_hand_raise(student_name)

    cv2.imshow("Hand Raise Detection and Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
