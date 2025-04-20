import os
import cv2
import json

def denormalize_bbox(image, bbox):
    image_height, image_width = image.shape[:2]
    class_id, x_center, y_center, width, height = bbox

    x_center *= image_width
    y_center *= image_height
    width *= image_width
    height *= image_height

    # Calculate corner points
    x1 = int(x_center - width / 2)
    y1 = int(y_center - height / 2)
    x2 = int(x_center + width / 2)
    y2 = int(y_center + height / 2)

    return class_id, x1, y1, x2, y2


def process_dataset(images_folder, bboxes_folder, output_json):
    dataset = []

    # Loop through each image in the folder
    for image_file in os.listdir(images_folder):
        if image_file.endswith((".jpg", ".jpeg")):
            image_path = os.path.join(images_folder, image_file)
            bbox_file = os.path.join(bboxes_folder, os.path.splitext(image_file)[0] + ".txt")

            # Check if the corresponding bounding box file exists
            if not os.path.exists(bbox_file):
                print(f"Bounding box file missing for {image_file}")
                continue

            # Load the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load {image_path}")
                continue

            # Read bounding box data from the text file
            with open(bbox_file, "r") as f:
                bboxes = []
                for line in f.readlines():
                    bbox = list(map(float, line.strip().split()))
                    bboxes.append(denormalize_bbox(image, bbox))

            # json structure
            entry = {
                "image": image_file,
                "width": image.shape[1],
                "height": image.shape[0],
                "bboxes": [
                    {"class_id": class_id, "x1": x1, "y1": y1, "x2": x2, "y2": y2}
                    for class_id, x1, y1, x2, y2 in bboxes
                ]
            }
            dataset.append(entry)

    # Save the dataset to a JSON file
    with open(output_json, "w") as json_file:
        json.dump(dataset, json_file, indent=4)
    print(f"Dataset saved to {output_json}")


# Example usage
images_folder = "./dataset/images/train"
bboxes_folder = "./dataset/labels/train"
output_json = "ground_truth.json"

process_dataset(images_folder, bboxes_folder, output_json)
