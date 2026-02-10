import os
import time
import cv2
import torch
from ultralytics import YOLO

def process_video(model_path, input_video, output_folder):
    model_name = os.path.basename(model_path)
    output_filename = f"output_{model_name}_{os.path.basename(input_video)}"
    output_path = os.path.join(output_folder, output_filename)
    
    print(f"Processing {input_video} with {model_name}...")
    
    try:
        # Load model
        # For ONNX, Ultralytics auto-detects based on extension
        model = YOLO(model_path, task='detect') 
        
        # Open video
        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            print(f"Error opening video {input_video}")
            return None

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Video Writer
        # Using webm/vp8 or mp4/avc1 depending on codec availability, trying mp4v first
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        start_time = time.time()
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Inference
            # device='cpu' to force CPU if needed, or let it auto-select
            results = model.predict(frame, verbose=False)
            
            # Plot results
            annotated_frame = results[0].plot()
            
            out.write(annotated_frame)
            frame_count += 1
            
            if frame_count % 50 == 0:
                print(f"  Processed {frame_count}/{total_frames} frames...")

        end_time = time.time()
        duration = end_time - start_time
        avg_fps = frame_count / duration if duration > 0 else 0
        
        cap.release()
        out.release()
        
        print(f"Saved {output_path}")
        print(f"Average FPS: {avg_fps:.2f}")
        
        return {
            "model": model_name,
            "fps": avg_fps,
            "total_time": duration,
            "status": "Success",
            "output_file": output_path
        }

    except Exception as e:
        print(f"Failed to process with {model_name}: {e}")
        return {
            "model": model_name,
            "fps": 0,
            "total_time": 0,
            "status": f"Failed: {str(e)}",
            "output_file": "N/A"
        }

def main():
    input_video = os.path.join(os.path.dirname(__file__), "Construction_Safety_Hazard_CCTV_Video.mp4")
    output_folder = os.path.join(os.path.dirname(__file__), "output_video_comparison")
    os.makedirs(output_folder, exist_ok=True)
    
    if not os.path.exists(input_video):
        print(f"Input video not found: {input_video}")
        return

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
            res = process_video(path, input_video, output_folder)
            results.append(res)
        else:
            print(f"Model {path} not found.")
            results.append({
                "model": m,
                "fps": 0,
                "total_time": 0,
                "status": "File Not Found",
                "output_file": "N/A"
            })

    # Generate Report
    report_path = os.path.join(os.path.dirname(__file__), "video_comparison_report.md")
    with open(report_path, "w") as f:
        f.write("# Video Inference Comparison Report\n\n")
        f.write(f"**Input Video**: `{os.path.basename(input_video)}`\n\n")
        f.write("| Model | Status | Avg FPS | Total Time (s) | Output |\n")
        f.write("|-------|--------|---------|----------------|--------|\n")
        for r in results:
            output_link = f"[Link]({os.path.basename(r['output_file'])})" if r['status'] == "Success" else "N/A"
            # Clean up error message for table
            status = r['status'].replace("|", " ")
            if len(status) > 50:
                 status = status[:47] + "..."
            f.write(f"| {r['model']} | {status} | {r['fps']:.2f} | {r['total_time']:.2f} | {output_link} |\n")
            
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()
