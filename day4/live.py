
import cv2
from ultralytics import YOLO
import time

# Load the YOLO model
model = YOLO('yolo26colourdataset.pt')

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Variables for FPS calculation
prev_time = 0
fps = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Perform inference on the frame
    results = model(frame)

    # Render the results on the frame
    annotated_frame = results[0].plot()

    # Calculate FPS
    current_time = time.time()
    if (current_time - prev_time) > 0:
        fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display the FPS on the frame
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('YOLO Live', annotated_frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
