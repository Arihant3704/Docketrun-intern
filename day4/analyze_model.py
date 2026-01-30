from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolo26colourdataset.pt')

print("--- YOLO Model Analysis ---")

# 1. Display class names
if model.names:
    print("\nDetectaable Classes:")
    for class_id, class_name in model.names.items():
        print(f"- {class_id}: {class_name}")
else:
    print("\nCould not retrieve class names from the model.")

# 2. Display input/output shapes (this information might be less direct for YOLO models as they are dynamic)
# For YOLOv8, input shape is usually inferred from the data or a default.
# The `model.predictor.dataset.shapes` or `model.predictor.dataset.imgsz` might give clues.
# For a more general approach, we can try to get an example input.
print("\nInput/Output Information (Inferred/Default):")
try:
    # Attempt to get input image size from model properties
    # This might vary based on ultralytics version or model export
    if hasattr(model, 'imgsz'):
        print(f"- Input image size (imgsz): {model.imgsz}")
    elif hasattr(model.model, 'imgsz'): # Access if stored in the underlying torch model
        print(f"- Input image size (model.model.imgsz): {model.model.imgsz}")
    else:
        print("- Input image size: Not directly available or inferred dynamically.")

    # Output details are typically detections (boxes, scores, class_ids)
    print("- Output: Detections (bounding boxes, confidence scores, class IDs per detected object)")

except Exception as e:
    print(f"Error retrieving input/output information: {e}")

print("\n--------------------------")
