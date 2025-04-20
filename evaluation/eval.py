import torch
import cv2
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import numpy as np
import json
import os

# Load the model
MODEL_PATH = "yolov5/runs/train/hand_raise_detector/weights/best.pt"  # Adjust path as needed
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)

# Paths
GROUND_TRUTH_PATH = "ground_truth.json"  # JSON file containing ground truth annotations
TEST_IMAGES_DIR = "./dataset/images/train"  # Directory containing test images

def load_ground_truth(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def is_box_match(gt_box, pred_box, iou_threshold=0.5):
    x1, y1, x2, y2 = gt_box
    px1, py1, px2, py2 = pred_box

    inter_x1 = max(x1, px1)
    inter_y1 = max(y1, py1)
    inter_x2 = min(x2, px2)
    inter_y2 = min(y2, py2)

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    gt_area = (x2 - x1) * (y2 - y1)
    pred_area = (px2 - px1) * (py2 - py1)

    union_area = gt_area + pred_area - inter_area
    iou = inter_area / union_area if union_area > 0 else 0

    return iou >= iou_threshold

def evaluate_model(ground_truth, test_images_dir, model):
    y_true = []
    y_pred = []

    for gt_data in ground_truth:  # Iterate over the list of ground truth data
        image_name = gt_data["image"]  # Get the image name
        image_path = os.path.join(test_images_dir, image_name)
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not read image: {image_path}")
            continue

        # Predict with the model
        results = model(img)
        pred_boxes = []
        pred_classes = []

        for detection in results.pred[0]:
            x1, y1, x2, y2, confidence, cls = detection.tolist()
            if confidence >= 0.5:  # Confidence threshold
                pred_boxes.append([x1, y1, x2, y2])
                pred_classes.append(int(cls))  # Class label

        # Compare predictions with ground truth
        gt_boxes = [(box["x1"], box["y1"], box["x2"], box["y2"]) for box in gt_data["bboxes"] if box["class_id"] == 0]
        gt_classes = [0] * len(gt_boxes)  # Class 0 = "hand_up"

        for gt_box in gt_boxes:
            matched = False
            for pred_box, pred_cls in zip(pred_boxes, pred_classes):
                if pred_cls == 0 and is_box_match(gt_box, pred_box):
                    matched = True
                    break
            y_true.append(1)  # True positive
            y_pred.append(1 if matched else 0)  # Predicted match or not

        # Handle false positives
        for pred_box, pred_cls in zip(pred_boxes, pred_classes):
            if pred_cls == 0 and all(not is_box_match(gt_box, pred_box) for gt_box in gt_boxes):
                y_true.append(0)
                y_pred.append(1)

        # Handle false negatives
        for gt_box in gt_boxes:
            if all(not is_box_match(gt_box, pred_box) for pred_box in pred_boxes):
                y_true.append(1)
                y_pred.append(0)

    # Calculate metrics
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)

    return precision, recall, f1, accuracy

if __name__ == "__main__":
    # Load ground truth data
    ground_truth = load_ground_truth(GROUND_TRUTH_PATH)

    # Evaluate the model
    precision, recall, f1, accuracy = evaluate_model(ground_truth, TEST_IMAGES_DIR, model)

    # Print the results
    print(f"Model Evaluation Metrics:")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")
    print(f"Accuracy: {accuracy:.2f}")
