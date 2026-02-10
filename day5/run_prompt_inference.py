import os
import cv2
import torch
from ultralytics import YOLO

def main():
    # Configuration
    model_path = os.path.join(os.path.dirname(__file__), "yoloe-26n-seg.pt")
    input_video = os.path.join(os.path.dirname(__file__), "Construction_Safety_Hazard_CCTV_Video.mp4")
    output_video = os.path.join(os.path.dirname(__file__), "output_harness_detection.mp4")
    
    prompt = ["harness on person"] # User requested prompt
    
    print(f"Loading model: {model_path}")
    try:
        model = YOLO(model_path)
        
        # Set text prompt
        print(f"Setting prompt: {prompt}")
        # Using the API pattern found in run.py
        model.set_classes(prompt, model.get_text_pe(prompt))
        
        # Process Video
        print(f"Processing video: {input_video}")
        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Predict
            results = model.predict(frame, verbose=False)
            
            # Visualize
            annotated_frame = results[0].plot()
            
            out.write(annotated_frame)
            frame_count += 1
            
            if frame_count % 50 == 0:
                print(f"Processed {frame_count}/{total_frames} frames...")
                
        cap.release()
        out.release()
        print(f"Done! Output saved to: {output_video}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
