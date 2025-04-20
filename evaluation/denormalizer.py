import cv2

def denormalize_bbox(image, bbox):
    image_height, image_width = image.shape[:2]
    _, x_center, y_center, width, height = bbox

    # Convert normalized coordinates to absolute pixel values
    x_center *= image_width
    y_center *= image_height
    width *= image_width
    height *= image_height

    # Calculate corner points
    x1 = int(x_center - width / 2)
    y1 = int(y_center - height / 2)
    x2 = int(x_center + width / 2)
    y2 = int(y_center + height / 2)

    return x1, y1, x2, y2


# test
image_path = "D:/misc/langs/python/new/yolov5/dataset/images/train/img1.jpg"
bboxes = [
    [0, 0.482083, 0.480000, 0.365833, 0.915000],
    [0, 0.870000, 0.501250, 0.260000, 0.997500],
    [0, 0.131250, 0.428750, 0.259167, 0.852500],
] 

image = cv2.imread(image_path)

for i in bboxes:
    x1, y1, x2, y2 = denormalize_bbox(image, i)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


cv2.imshow("Bounding Boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
