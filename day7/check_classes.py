from ultralytics import YOLO
import sys

try:
    model = YOLO('/home/arihant/intern/day7/best.pt')
    print("Classes:", model.names)
except Exception as e:
    print(f"Error: {e}")
