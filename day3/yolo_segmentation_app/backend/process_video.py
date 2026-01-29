from ultralytics import YOLO
import cv2
import os

model_path = "/home/arihant/intern/day3/yolo_segmentation_app/backend/model/best.pt"
input_path = "/home/arihant/intern/day3/yolo_segmentation_app/Safety_Harness_the_Right_Way_480P.mp4"
output_dir = "/home/arihant/intern/day3/yolo_segmentation_app/backend/results"
output_filename = "Safety_Harness_the_Right_Way_480P_pred.mp4"
output_path = os.path.join(output_dir, output_filename)

os.makedirs(output_dir, exist_ok=True)

model = YOLO(model_path)
print(f"Running inference on {input_path}...")

# Run inference
results = model(input_path, stream=True, conf=0.25)

# Process and save
cap = cv2.VideoCapture(input_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Use 'avc1' or 'mp4v' - mp4v is usually safer for local cv2
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

for result in results:
    annotated_frame = result.plot()
    out.write(annotated_frame)

cap.release()
out.release()
print(f"Saved processed video to {output_path}")
