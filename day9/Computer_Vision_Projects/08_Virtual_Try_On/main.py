
import cv2
import numpy as np
import mediapipe as mp
import os
import sys

def overlay_transparent(background, overlay, x, y, overlay_size=None):
    """
    Overlays a transparent PNG (or image with alpha) onto a background.
    """
    bg_h, bg_w, _ = background.shape
    
    if overlay_size is not None:
        overlay = cv2.resize(overlay, overlay_size)
    
    h, w, c = overlay.shape
    
    if x >= bg_w or y >= bg_h:
        return background
    
    if x + w > bg_w:
        w = bg_w - x
        overlay = overlay[:, :w]
        
    if y + h > bg_h:
        h = bg_h - y
        overlay = overlay[:h]
    
    if c < 4:
        gray = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)
        overlay[:, :, 3] = mask
        
    alpha = overlay[:, :, 3] / 255.0
    
    for c in range(0, 3):
        background[y:y+h, x:x+w, c] = (alpha * overlay[:, :, c] + 
                                       (1.0 - alpha) * background[y:y+h, x:x+w, c])
                                       
    return background

def draw_mannequin(img):
    """
    Draws a realistic-ish mannequin on the image for mock output.
    """
    # Skin color
    skin_color = (180, 200, 225) # BGR
    
    # Head
    cv2.ellipse(img, (640, 150), (40, 50), 0, 0, 360, skin_color, -1)
    
    # Neck
    cv2.rectangle(img, (620, 200), (660, 230), skin_color, -1)
    
    # Shoulders/Torso base (Gray undershirt area)
    cv2.ellipse(img, (640, 260), (90, 40), 0, 0, 360, skin_color, -1)
    
    # Arms
    # Left Arm
    cv2.line(img, (550, 260), (450, 400), skin_color, 25)
    # Right Arm (raised slightly as if selecting)
    cv2.line(img, (730, 260), (850, 350), skin_color, 25)
    
    # Legs (Torso extends down)
    cv2.rectangle(img, (580, 500), (700, 720), (50, 50, 50), -1) # Pants
    
    return img

def main():
    # Load Shirt Assets
    shirt_files = [f"Resources/shirt_{i}.png" for i in range(5)]
    shirts = []
    
    # Ensure assets exist
    for f in shirt_files:
        if os.path.exists(f):
            shirts.append(cv2.imread(f, cv2.IMREAD_UNCHANGED))
        else:
            print(f"Warning: {f} not found.")

    if not shirts:
        print("No shirt assets found. Exiting.")
        return

    current_shirt_id = 0
    
    # Setup Camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    
    # Button Configuration
    button_radius = 40
    button_margin = 100
    button_x = 1150
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.flip(img, 1) # Mirror view for interaction
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        
        h, w, c = img.shape
        
        # UI Constants
        sidebar_x = int(w * 0.85) # 85% of width (Right side)
        zone_height = int(h / 5)  # Divide screen height into 5 zones
        
        # Draw UI Sidebar (Zones)
        overlay = img.copy()
        cv2.rectangle(overlay, (sidebar_x, 0), (w, h), (50, 50, 50), -1)
        img = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)
        
        for i in range(len(shirts)):
            y1 = i * zone_height
            y2 = (i + 1) * zone_height
            
            # Highlight selected zone
            color = (200, 200, 200)
            thickness = 2
            if i == current_shirt_id:
                color = (0, 255, 0)
                thickness = -1 # Fill
                # Draw "Selected" background
                cv2.rectangle(img, (sidebar_x, y1), (w, y2), (0, 100, 0), -1)
            
            cv2.rectangle(img, (sidebar_x, y1), (w, y2), color, 2)
            cv2.putText(img, f"Shirt {i+1}", (sidebar_x + 20, int((y1+y2)/2)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # --- Interaction Logic (Both Wrists) ---
            wrists = [landmarks[16], landmarks[15]] # Right, Left
            
            for wrist in wrists:
                wx, wy = int(wrist.x * w), int(wrist.y * h)
                
                # Check if wrist is in the Sidebar Zone
                if wx > sidebar_x:
                    # Provide visual feedback cursor
                    cv2.circle(img, (wx, wy), 20, (0, 255, 255), -1)
                    
                    # Determine which zone (0-4)
                    selected_zone = int(wy / zone_height)
                    selected_zone = max(0, min(selected_zone, 4)) # Clamp 0-4
                    
                    current_shirt_id = selected_zone

            # --- Try-On Logic (Shoulders) ---
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            
            lm_11 = (int(left_shoulder.x * w), int(left_shoulder.y * h))
            lm_12 = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            
            # Shoulder width
            shoulder_width = int(abs(lm_11[0] - lm_12[0]))
            
            # If scaling is robust
            if shoulder_width > 20: 
                current_shirt = shirts[current_shirt_id]
                
                # Scale shirt
                shirt_width = int(shoulder_width * 1.5) # Dynamic scale
                shirt_ratio = current_shirt.shape[0] / current_shirt.shape[1]
                shirt_height = int(shirt_width * shirt_ratio)
                
                center_x = (lm_11[0] + lm_12[0]) // 2
                top_left_x = center_x - (shirt_width // 2)
                
                # Anchor shirt slightly below shoulder line midpoint
                # Adjust formula to align "neck" of shirt with real neck (approx mid shoulders)
                top_left_y = int((lm_11[1] + lm_12[1]) / 2) - int(shirt_height * 0.15)
                
                img = overlay_transparent(img, current_shirt, top_left_x, top_left_y, (shirt_width, shirt_height))
                
        cv2.imshow("Virtual Try-On", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Support mock run
    if len(sys.argv) > 1 and sys.argv[1] == "mock":
        print("Generating realistic mock output...")
        
        # Load valid shirt
        shirt_files = [f"Resources/shirt_{i}.png" for i in range(5)]
        
        # Load realistic mannequin
        mannequin_path = "Resources/mannequin.jpg"
        if os.path.exists(mannequin_path):
            img = cv2.imread(mannequin_path)
            img = cv2.resize(img, (1280, 720)) # Resize to match logic
        else:
            print("Mannequin not found, drawing fallback.")
            img = np.zeros((720, 1280, 3), dtype=np.uint8)
            img[:] = (240, 240, 240)
            img = draw_mannequin(img)

        # Process the static image through MediaPipe to find landmarks
        mpPose = mp.solutions.pose
        pose = mpPose.Pose(static_image_mode=True, min_detection_confidence=0.5)
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        
        h, w, c = img.shape
        
        # Draw Shirt Overlay if landmarks found
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            
            lm_11 = (int(left_shoulder.x * w), int(left_shoulder.y * h))
            lm_12 = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            
            shoulder_width = int(abs(lm_11[0] - lm_12[0]))
            
            # Use shirt_0 (Red/Real)
            current_shirt = cv2.imread(shirt_files[0], cv2.IMREAD_UNCHANGED)
            
            if shoulder_width > 20 and current_shirt is not None:
                shirt_width = int(shoulder_width * 1.5)
                shirt_ratio = current_shirt.shape[0] / current_shirt.shape[1]
                shirt_height = int(shirt_width * shirt_ratio)
                
                center_x = (lm_11[0] + lm_12[0]) // 2
                top_left_x = center_x - (shirt_width // 2)
                top_left_y = int((lm_11[1] + lm_12[1]) / 2) - int(shirt_height * 0.15)
                
                img = overlay_transparent(img, current_shirt, top_left_x, top_left_y, (shirt_width, shirt_height))
        
        # Draw New Sidebar UI for Mock
        h, w, c = img.shape
        sidebar_x = int(w * 0.85)
        zone_height = int(h / 5)
        
        overlay = img.copy()
        cv2.rectangle(overlay, (sidebar_x, 0), (w, h), (50, 50, 50), -1)
        img = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)
        
        for i in range(5):
            y1 = i * zone_height
            y2 = (i + 1) * zone_height
            
            color = (200, 200, 200)
            if i == 0: # Highlight first one
                cv2.rectangle(img, (sidebar_x, y1), (w, y2), (0, 100, 0), -1)
                color = (0, 255, 0)
            
            cv2.rectangle(img, (sidebar_x, y1), (w, y2), color, 2)
            cv2.putText(img, f"Shirt {i+1}", (sidebar_x + 20, int((y1+y2)/2)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        
        cv2.imwrite("output.jpg", img)
        print("Saved output.jpg")
    else:
        main()
