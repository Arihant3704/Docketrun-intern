import cv2
from ultralytics import YOLO
import time
import numpy as np

def process_video_with_fps(model_path, video_path, output_path):
    # Load the YOLO model
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # To calculate average FPS
    frame_times = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()

        # Run YOLOv8 inference on the frame
        results = model(frame, stream=True)

        # Get the annotated frame
        for r in results:
            annotated_frame = r.plot()

        end_time = time.time()
        
        # Calculate FPS
        frame_time = end_time - start_time
        frame_times.append(frame_time)
        
        # Use a moving average for smoother FPS display
        if len(frame_times) > 30: # average over last 30 frames
            avg_fps = 1.0 / np.mean(frame_times[-30:])
        else:
            avg_fps = 1.0 / np.mean(frame_times) if frame_times else 0

        # Draw the FPS on the frame
        cv2.putText(annotated_frame, f"FPS: {avg_fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Write the frame with annotations and FPS
        out.write(annotated_frame)

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python process_video_with_fps.py <model_path> <video_path> <output_path>")
        sys.exit(1)

    model_path = sys.argv[1]
    video_path = sys.argv[2]
    output_path = sys.argv[3]

    process_video_with_fps(model_path, video_path, output_path)
