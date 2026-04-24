from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

VEHICLE_CLASSES = [2, 3, 5, 7]

def count_vehicles(frame):
    results = model(frame, conf=0.3, verbose=False)
    count = 0

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            if cls in VEHICLE_CLASSES and conf > 0.2:
                count += 1

    return count


def get_density(count):
    if count < 5:
        return "LOW"
    elif count < 10:
        return "MEDIUM"
    else:
        return "HIGH"