from ultralytics import YOLO
import sys
import os
import cv2

def detect_objects(image_path, output_path='output.jpg'):
    # Load a pretrained YOLOv8n model
    model = YOLO("yolov8n.pt")

    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    # Run inference
    results = model(image_path)

    # Process results
    for result in results:
        # Visualize the results on the frame
        im_array = result.plot()  # plot a BGR numpy array of predictions
        cv2.imwrite(output_path, im_array)  # save image
        print(f"Detections completed. Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        detect_objects(sys.argv[1])
    else:
        if os.path.exists("input.jpg"):
            detect_objects("input.jpg")
        else:
            print("Usage: python main.py <image_path>")
