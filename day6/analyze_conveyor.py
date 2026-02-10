import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque

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

    # Material classes (Based on checks of model.names: {0: 'Belt', 1: 'belt', 2: 'mineral', 3: 'roller'})
    # We assume 'mineral' represents the material on the belt.
    material_classes = ['mineral']
    
    # Tracking data
    # Store recent centroids for each object ID: {id: deque([(x, y), ...], maxlen=10)}
    track_history = {}
    
    # Belt status parameters
    movement_threshold = 2.0  # Pixels per frame avg to consider moving
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, verbose=False)
        
        material_present = False
        moving_objects_count = 0
        total_tracked_objects = 0
        
        if results and results[0].boxes:
            boxes = results[0].boxes
            
            # Check for material presence
            for cls_id in boxes.cls:
                class_name = model.names[int(cls_id)]
                if class_name in material_classes:
                    material_present = True
            
            # Check for movement using tracking IDs
            if boxes.id is not None:
                track_ids = boxes.id.int().cpu().tolist()
                cls_ids = boxes.cls.int().cpu().tolist()
                xywhs = boxes.xywh.cpu().tolist() # Center x, Center y, Width, Height
                
                for track_id, cls_id, xywh in zip(track_ids, cls_ids, xywhs):
                    class_name = model.names[cls_id]
                    
                    # focus movement detection on material on the belt
                    if class_name in material_classes:
                        total_tracked_objects += 1
                        cx, cy = xywh[0], xywh[1]
                        
                        if track_id not in track_history:
                            track_history[track_id] = deque(maxlen=5)
                        
                        track_history[track_id].append((cx, cy))
                        
                        # Calculate movement if we have enough history
                        if len(track_history[track_id]) >= 2:
                            # Calculate distance between last two points
                            p1 = track_history[track_id][-2]
                            p2 = track_history[track_id][-1]
                            dist = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
                            
                            if dist > movement_threshold:
                                moving_objects_count += 1

        # Determine Belt Status
        # User request: "keep belt as moving"
        belt_status = "MOVING"

        # Visualize
        annotated_frame = results[0].plot()

        # Overlay Info
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Material Status
        mat_text = f"Material: {'YES' if material_present else 'NO'}"
        mat_color = (0, 255, 0) if material_present else (0, 0, 255)
        cv2.putText(annotated_frame, mat_text, (20, 50), font, 1.2, mat_color, 3)
        
        # Belt Status
        belt_color = (0, 255, 0) # Green for moving
        cv2.putText(annotated_frame, f"Belt: {belt_status}", (20, 100), font, 1.2, belt_color, 3)

        out.write(annotated_frame)
        
        # Optional: Display (commented out for headless/batch run)
        # cv2.imshow("YOLO Inference", annotated_frame)
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processing complete. Output saved to {output_path}")

if __name__ == "__main__":
    # Paths relative to the script location or valid absolute paths
    video_path = "convery belt/1.mp4"
    model_path = "convery belt/best.pt"
    output_path = "convery belt/output_1.mp4"
    
    print("Starting analysis...")
    analyze_video(video_path, output_path, model_path)
