import time
import os
import torch
import numpy as np
from ultralytics import YOLO

def benchmark_model(model_path, image_path, device='cpu', runs=50):
    print(f"Benchmarking {model_path} on {device}...")
    try:
        model = YOLO(model_path, task='detect') # task='detect' or 'segment', auto-inferred usually
        
        # Warmup
        for _ in range(10):
            model.predict(image_path, verbose=False, device=device)
            
        # Timing
        start_time = time.time()
        for _ in range(runs):
            results = model.predict(image_path, verbose=False, device=device)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / runs * 1000 # ms
        fps = 1000 / avg_time
        
        # Get accuracy metrics (confidence of top detection) from the last result
        # This is a rough proxy for accuracy retention
        result = results[0]
        if len(result.boxes) > 0:
            top_conf = float(result.boxes.conf[0])
            num_detections = len(result.boxes)
        else:
            top_conf = 0.0
            num_detections = 0
            
        return {
            "model": os.path.basename(model_path),
            "size_mb": os.path.getsize(model_path) / (1024 * 1024),
            "avg_time_ms": avg_time,
            "fps": fps,
            "top_confidence": top_conf,
            "num_detections": num_detections
        }
    except Exception as e:
        print(f"Error benchmarking {model_path}: {e}")
        return None

def main():
    image_path = os.path.join(os.path.dirname(__file__), "1.jpg")
    if not os.path.exists(image_path):
        # Fallback to creating a dummy image if 1.jpg doesn't exist
        from PIL import Image
        img = Image.new('RGB', (640, 640), color = 'red')
        image_path = os.path.join(os.path.dirname(__file__), "benchmark_dummy.jpg")
        img.save(image_path)
        print("Created dummy benchmark image.")

    models = [
        "yolo26colourdataset.pt",
        "yolo26colourdataset.onnx",
        "yolo26colourdataset_half.onnx",
        "yoloe-26n-seg.pt",
        "yoloe-26n-seg.onnx",
        "yoloe-26n-seg_half.onnx"
    ]
    
    results = []
    
    for m in models:
        path = os.path.join(os.path.dirname(__file__), m)
        if os.path.exists(path):
            res = benchmark_model(path, image_path, runs=30)
            if res:
                results.append(res)
        else:
            print(f"Model {path} not found.")

    # Generate Markdown Report
    report_path = os.path.join(os.path.dirname(__file__), "benchmark_report.md")
    with open(report_path, "w") as f:
        f.write("# Model Benchmark Report\n\n")
        f.write("| Model | Size (MB) | Avg Time (ms) | FPS | Top Conf | Detections |\n")
        f.write("|-------|-----------|---------------|-----|----------|------------|\n")
        for r in results:
            f.write(f"| {r['model']} | {r['size_mb']:.2f} | {r['avg_time_ms']:.2f} | {r['fps']:.2f} | {r['top_confidence']:.4f} | {r['num_detections']} |\n")
    
    print(f"Benchmark report saved to {report_path}")
    print(open(report_path).read())

if __name__ == "__main__":
    main()
