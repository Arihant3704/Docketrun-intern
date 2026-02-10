from ultralytics import YOLO

# 1. Load the model
model = YOLO("yolov8l-worldv2.pt")

# 2. Define custom classes (Open-Vocabulary feature)
model.set_classes(["person","Convery-belt", "object", "coal", "stone"])

# 3. Run tracking on those specific classes
results = model.track(source="b1.mp4", imgsz=640, show=True)
