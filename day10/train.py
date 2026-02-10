from ultralytics import YOLO
import os
import yaml
import tkinter as tk
from tkinter import filedialog

def train_model():
    print("Select the dataset DIRECTORY (e.g., car_dataset)")
    root = tk.Tk()
    root.withdraw()
    dataset_dir = filedialog.askdirectory(title="Select Dataset Directory")
    
    if not dataset_dir:
        print("No dataset selected.")
        return

    # Check structure
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")
    
    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        print(f"Error: {dataset_dir} does not contain 'images' and 'labels' folders.")
        return

    # Create data.yaml for YOLO
    # We infer class name from directory name usually, or default to 1 class
    # simple_labeler sets class_id=0 for everything.
    class_name = os.path.basename(dataset_dir).replace("_dataset", "")
    data = {
        'path': dataset_dir,
        'train': 'images',
        'val': 'images', # Use same for val for simplicity in this demo
        'names': {
            0: class_name
        }
    }
    
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f)
        
    print(f"Created data.yaml at {yaml_path}")
    
    # Train
    print("Starting training (YOLOv8n-seg)...")
    model = YOLO('yolov8n-seg.pt') # Load model
    
    # Train
    results = model.train(
        data=yaml_path,
        epochs=10,
        imgsz=640,
        batch=4,
        project=os.path.join(dataset_dir, "runs"),
        name="train"
    )
    
    print("Training Complete!")
    print(f"Results saved to {os.path.join(dataset_dir, 'runs', 'train')}")

if __name__ == "__main__":
    train_model()
