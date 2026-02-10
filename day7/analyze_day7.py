import cv2
import numpy as np
from ultralytics import YOLO

def analyze_video(input_path, output_path, model_path):
    # Load the YOLO model
    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Initialize VideoWriter
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    BELT_CLASSES = ['Belt', 'belt']

    # Optical Flow Parameters
    prev_gray = None
    belt_moving = False
    movement_threshold = 1.0 # Sensitivity for optical flow magnitude
    
    # Coal Detection Parameters
    coal_present = False
    EDGE_THRESHOLD = 5075 # Adjust based on debug output
    
    # Process frames
    frame_count = 0
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            frame_count += 1
            
            # 1. Run YOLO Detection
            results = model(frame, verbose=False)
            boxes = results[0].boxes
            
            coal_present = False
            belt_box = None
            
            # 2. Parse Detections
            if boxes:
                for box in boxes:
                    cls_id = int(box.cls[0])
                    cls_name = model.names[cls_id]
                    
                    # Check for Belt (get largest one if multiple)
                    if cls_name in BELT_CLASSES:
                        if belt_box is None:
                            belt_box = box.xyxy[0].cpu().numpy().astype(int) # x1, y1, x2, y2

            # 3. Check Belt Movement & Coal Presence
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            current_belt_moving = False
            
            if belt_box is not None:
                x1, y1, x2, y2 = belt_box
                # Ensure coords are within frame
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(width, x2), min(height, y2)
                
                # Crop Belt ROI
                belt_roi = gray[y1:y2, x1:x2]
                
                # A. Optical Flow for Movement
                if prev_gray is not None:
                    # Resize prev_gray ROI if shape mismatch (rare but possible if belt box fluctuates)
                    prev_belt_roi = prev_gray[y1:y2, x1:x2]
                    
                    if belt_roi.shape == prev_belt_roi.shape and belt_roi.size > 0:
                        flow = cv2.calcOpticalFlowFarneback(prev_belt_roi, belt_roi, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                        avg_mag = np.mean(mag)
                        
                        if avg_mag > movement_threshold:
                            current_belt_moving = True
                
                # B. Canny Edge Detection for Coal
                # Blur to remove noise
                blurred_roi = cv2.GaussianBlur(belt_roi, (5, 5), 0)
                # Detect edges
                edges = cv2.Canny(blurred_roi, 50, 150)
                edge_count = cv2.countNonZero(edges)
                
                if edge_count > EDGE_THRESHOLD:
                    coal_present = True
                    
                # Debugging threshold
                if frame_count % 30 == 0:
                     print(f"Frame {frame_count}: Edge Count = {edge_count} -> Coal: {coal_present}")

            else:
                # Fallback for movement
                current_belt_moving = belt_moving 
                # Fallback for coal
                coal_present = False

            belt_moving = current_belt_moving
            prev_gray = gray.copy()

            # 4. Annotate Frame
            annotated_frame = results[0].plot()
            
            # Overlay Status
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # Coal Status
            if coal_present:
                cv2.putText(annotated_frame, "Object is present", (50, 50), font, 1.5, (0, 0, 255), 3)
            else:
                 cv2.putText(annotated_frame, "No Object", (50, 50), font, 1.5, (0, 255, 0), 3)

            # Belt Status
            status_text = "Belt: MOVING" if belt_moving else "Belt: NOT MOVING"
            status_color = (0, 255, 0) if belt_moving else (0, 0, 255)
            cv2.putText(annotated_frame, status_text, (50, 100), font, 1.5, status_color, 3)

            out.write(annotated_frame)
            
            if frame_count % 30 == 0:
                print(f"Processed {frame_count} frames...")

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        cap.release()
        out.release()
        print(f"Analysis Complete. Saved to {output_path}")

if __name__ == "__main__":
    # Define paths
    video_path = "/home/arihant/intern/day7/a.mp4"
    model_path = "/home/arihant/intern/day7/best.pt"
    output_path = "/home/arihant/intern/day7/output_a.mp4"
    
    analyze_video(video_path, output_path, model_path)
