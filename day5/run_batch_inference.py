import os
import cv2
import torch
from ultralytics import YOLO

def process_video(model, input_path, output_path, prompt):
    print(f"Processing {input_path}...")
    try:
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open {input_path}")
            return False

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30 # Fallback
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Using mp4v for compatibility
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
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
                print(f"  {frame_count}/{total_frames} frames...")
                
        cap.release()
        out.release()
        print(f"Saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def main():
    # Configuration
    model_name = "yoloe-26n-seg.pt"
    model_path = os.path.join(os.path.dirname(__file__), model_name)
    
    videos = ["1.webm", "2.webm", "3.webm"]
    prompt = ["harness on person"]
    
    print(f"Loading model: {model_path}")
    try:
        model = YOLO(model_path)
        
        # Try setting prompt (might fail if model doesn't support it)
        try:
            print(f"Setting prompt: {prompt}")
            model.set_classes(prompt, model.get_text_pe(prompt))
        except AttributeError:
            print("Model does not support text prompts (get_text_pe/set_classes missing). Running standard inference.")
        except Exception as e:
            print(f"Warning setting prompt: {e}. Proceeding with standard inference.")
            
        output_dir = os.path.join(os.path.dirname(__file__), "output_batch")
        os.makedirs(output_dir, exist_ok=True)
        
        for vid in videos:
            input_path = os.path.join(os.path.dirname(__file__), vid)
            output_filename = f"output_{model_name}_{vid}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            if os.path.exists(input_path):
                process_video(model, input_path, output_path, prompt)
            else:
                print(f"Video not found: {input_path}")
                
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
