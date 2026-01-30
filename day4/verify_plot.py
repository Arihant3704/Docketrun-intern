import cv2
import numpy as np
from ultralytics import YOLO
import sys

def test_plot():
    try:
        # Create a dummy image (black)
        img = np.zeros((640, 640, 3), dtype=np.uint8)
        
        # Load model (using yolov8n.pt as it is standard and small)
        model = YOLO("yolov8n.pt")
        
        # Run inference
        results = model(img)
        
        # Simulate the change
        if results[0].boxes is not None:
             results[0].boxes.id = None
        
        # Test plot with line_width
        res_plot = results[0].plot(line_width=2)
        
        print("Success: plot() ran without error.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_plot())
