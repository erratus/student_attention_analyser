import sys
from pathlib import Path
import torch
import cv2
# yolov5_path = Path('D:/misc/langs/python/new/yolov5')  # Adjust to your YOLOv5 folder path
# sys.path.append(str(yolov5_path))

from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

device = select_device('cpu')  #0-gpu,'cpu'-cpu 
model = DetectMultiBackend('hand_raise_detector_valid/weights/best.pt', device=device)
model.eval()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access the camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Preprocess 
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    img = img.to(device)

    pred = model(img)
    pred = non_max_suppression(pred, 0.25, 0.45)  # Confidence threshold: 0.25, IoU threshold: 0.45

    #bounding boxes and labels
    for det in pred:
        if det is not None and len(det):
            for *xyxy, conf, cls in det:
                if conf > 0.5:  # Only draw boxes with confidence > 0.5
                    label = f"Hand Raise: {conf:.2f}"
                    cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Hand Raise Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
