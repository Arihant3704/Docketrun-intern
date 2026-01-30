
import cv2
from ultralytics import YOLO
import time
import numpy as np
import sys
import torch

def process_video(model_path, video_path, output_path, tracker=None, conf=0.25):
    # Load the YOLO model
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 inference on the frame
        if tracker:
            results = model.track(frame, persist=True, tracker=tracker, conf=conf)
        else:
            results = model(frame, conf=conf)

        if results[0].boxes is not None and results[0].boxes.is_track:
             # Remove the track_id column to hide ID in plot
             # data is [x1, y1, x2, y2, track_id, conf, cls] (7 cols)
             # keeping [x1, y1, x2, y2, conf, cls]
             boxes = results[0].boxes
             new_data = torch.cat((boxes.data[:, :4], boxes.data[:, 5:]), dim=1)
             results[0].boxes = boxes.__class__(new_data, boxes.orig_shape)

        # Get the annotated frame
        annotated_frame = results[0].plot(line_width=2)

        # Write the frame with annotations
        out.write(annotated_frame)

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python run_yolo.py <model_path> <video_path> <output_path> [tracker] [conf]")
        sys.exit(1)

    model_path = sys.argv[1]
    video_path = sys.argv[2]
    output_path = sys.argv[3]
    
    tracker = None
    if len(sys.argv) > 4:
        tracker = sys.argv[4]

    conf = 0.25
    if len(sys.argv) > 5:
        conf = float(sys.argv[5])

    process_video(model_path, video_path, output_path, tracker, conf)
