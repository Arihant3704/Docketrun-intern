import cv2
import numpy as np
import os
import sys
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from backend import SAM2Backend
import shutil

# Initialize Backend
try:
    backend = SAM2Backend()
except Exception as e:
    print(f"Failed to initialize backend: {e}")
    sys.exit(1)

# --- UI COLORS ---
COLORS = [
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0), (0, 128, 128), (128, 0, 128)
]

class SetupDialog:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Setup")
        self.video_path = None
        self.class_name = None
        
        # Video Selection
        tk.Label(root, text="Video Path:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.video_entry = tk.Entry(root, width=40)
        self.video_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_video).grid(row=0, column=2, padx=10, pady=10)
        
        # Initial Class Name
        tk.Label(root, text="Initial Class Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.class_entry = tk.Entry(root, width=40)
        self.class_entry.insert(0, "object")
        self.class_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Start Button
        tk.Button(root, text="Start Labeling", command=self.start, bg="green", fg="white").grid(row=2, column=1, pady=20)
        
    def browse_video(self):
        filename = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if filename:
            self.video_path = filename
            self.video_entry.delete(0, tk.END)
            self.video_entry.insert(0, filename)
            
    def start(self):
        self.video_path = self.video_entry.get()
        self.class_name = self.class_entry.get()
        
        if not self.video_path or not os.path.exists(self.video_path):
            messagebox.showerror("Error", "Please select a valid video file.")
            return
            
        if not self.class_name:
            messagebox.showerror("Error", "Please enter a class name.")
            return
            
        self.root.quit()
        self.root.destroy()

def show_setup_dialog():
    root = tk.Tk()
    app = SetupDialog(root)
    root.mainloop()
    return app.video_path, app.class_name

def main():
    # 1. Setup
    video_path, initial_class_name = show_setup_dialog()
    
    if not video_path or not initial_class_name:
        print("Setup cancelled.")
        return
        
    print(f"Loading video: {video_path}")
    backend.set_video(video_path)
    
    # --- State ---
    current_frame_idx = 0
    total_frames = backend.get_num_frames()
    
    # Object Management
    # obj_id -> class_name
    objects_registry = {1: initial_class_name} 
    current_obj_id = 1
    
    # Store prompts: {frame_idx: {obj_id: [(x, y, label), ...]}}
    prompts_store = {} 
    
    # Store masks: {frame_idx: {obj_id: mask_image}}
    cached_masks = {}
    
    # Settings
    skip_step = 5
    
    window_name = "SAM 2 Video Labeler"
    cv2.namedWindow(window_name)
    
    def get_prompts(frame, obj):
        if frame not in prompts_store: prompts_store[frame] = {}
        if obj not in prompts_store[frame]: prompts_store[frame][obj] = []
        return prompts_store[frame][obj]

    def add_prompt(frame, obj, x, y, label):
        get_prompts(frame, obj).append((x, y, label))

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            action = 1 # Positive
        elif event == cv2.EVENT_RBUTTONDOWN:
            action = 0 # Negative
        else:
            return
            
        add_prompt(current_frame_idx, current_obj_id, x, y, action)
        update_inference_for_current_frame()

    cv2.setMouseCallback(window_name, mouse_callback)
    
    def update_inference_for_current_frame():
        p_list = get_prompts(current_frame_idx, current_obj_id)
        if not p_list: return

        points = np.array([[p[0], p[1]] for p in p_list], dtype=np.float32)
        labels = np.array([p[2] for p in p_list], dtype=np.int32)
        
        try:
            mask = backend.add_point(current_frame_idx, points, labels, obj_id=current_obj_id)
            if mask.ndim == 3: mask = mask[0]
            if mask.ndim == 3: mask = mask[0]
            
            if current_frame_idx not in cached_masks: cached_masks[current_frame_idx] = {}
            cached_masks[current_frame_idx][current_obj_id] = mask
        except Exception as e:
            print(f"Inference error: {e}")

    def run_propagation(start_frame, max_steps=None):
        print(f"Propagating from frame {start_frame} (Max steps: {max_steps})...")
        # If running full propagation, show loading
        if max_steps is None or max_steps > 5:
            popup = tk.Toplevel()
            tk.Label(popup, text="Propagating...").pack(padx=20, pady=20)
            popup.update()
        else:
            popup = None

        count = 0
        try:
            for frame_idx, obj_ids, masks in backend.propagate(start_frame_idx=start_frame, max_frames=max_steps):
                if frame_idx not in cached_masks: cached_masks[frame_idx] = {}
                
                # Masks is (N_objs, H, W) or (N_objs, 1, H, W)
                # obj_ids gives the IDs
                
                # Squeeze extra dims if needed
                if masks.ndim == 4: masks = masks.squeeze(1) # (N, H, W)
                
                for i, obj_id in enumerate(obj_ids):
                    mask = masks[i] 
                    cached_masks[frame_idx][obj_id] = mask
                
                count += 1
        except Exception as e:
            print(f"Prop Error: {e}")
        finally:
            if popup: popup.destroy()
        print(f"Propagated {count} frames.")
        return count

    def create_new_object():
        nonlocal current_obj_id
        # Ask for name
        root = tk.Tk()
        root.withdraw()
        new_name = simpledialog.askstring("New Object", "Enter Class Name (e.g., person):")
        if new_name:
            # Increment ID
            # In SAM 2, object IDs are arbitrary integers. We just pick next available.
            next_id = max(objects_registry.keys()) + 1
            objects_registry[next_id] = new_name
            current_obj_id = next_id
            print(f"Switched to New Object: ID {current_obj_id} ({new_name})")

    def export_data():
        if not cached_masks:
             messagebox.showwarning("Warning", "No masks generated. Run propagation first.")
             return
             
        base_dir = os.path.dirname(video_path)
        # Use first class name as dataset name or 'mixed'
        ds_name = list(objects_registry.values())[0] if len(objects_registry) == 1 else "mixed"
        export_dir = os.path.join(base_dir, f"{ds_name}_dataset") 
        images_dir = os.path.join(export_dir, "images")
        labels_dir = os.path.join(export_dir, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        
        # We need a data.yaml or classes.txt to map ID -> Name?
        # Standard YOLO usually maps class index (0, 1, 2) to names in yaml.
        # We should generate a classes.txt mapping our runtime IDs to 0-indexed classes.
        
        # Map: runtime_obj_id -> yolo_class_index
        # We group by Name. 
        # e.g. ID 1='car', ID 2='car' -> Both are class 0
        unique_classes = sorted(list(set(objects_registry.values())))
        class_to_idx = {name: i for i, name in enumerate(unique_classes)}
        
        # Save data.yaml content hint
        yaml_content = f"names: {unique_classes}\npath: {export_dir}\ntrain: images\nval: images\n"
        with open(os.path.join(export_dir, "data_hint.yaml"), "w") as f:
            f.write(yaml_content)
            
        count = 0
        for frame_idx, objs_dict in cached_masks.items():
            if not objs_dict: continue
            
            frame_path = backend.get_frame(frame_idx)
            if not frame_path: continue
            
            # Copy Image
            shutil.copy(frame_path, os.path.join(images_dir, os.path.basename(frame_path)))
            
            # Create Label File
            h, w = 0, 0
            lines = []
            
            # Collect all objects in this frame
            for obj_id, mask in objs_dict.items():
                if mask.max() == 0: continue
                
                h, w = mask.shape[-2:]
                class_name = objects_registry.get(obj_id, "unknown")
                class_idx = class_to_idx.get(class_name, 0)
                
                mask_uint8 = (mask > 0).astype(np.uint8) * 255
                contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for cnt in contours:
                    if len(cnt) < 3: continue
                    cnt = cnt.reshape(-1, 2)
                    norm_points = []
                    for pt in cnt:
                        nx = pt[0] / w
                        ny = pt[1] / h
                        norm_points.extend([nx, ny])
                    
                    lines.append(f"{class_idx} {' '.join(map(str, norm_points))}\n")
            
            if lines:
                label_path = os.path.join(labels_dir, os.path.basename(frame_path).replace(".jpg", ".txt"))
                with open(label_path, "w") as f:
                    f.writelines(lines)
                count += 1
                
        messagebox.showinfo("Export Complete", f"Saved {count} labeled frames.\nValid Classes: {unique_classes}")

    # Main Loop
    while True:
        frame_path = backend.get_frame(current_frame_idx)
        if not frame_path: break
        img = cv2.imread(frame_path)
        if img is None: break
        
        # 1. Overlay Masks
        if current_frame_idx in cached_masks:
            for obj_id, mask in cached_masks[current_frame_idx].items():
                if mask.max() > 0:
                    color = COLORS[(obj_id - 1) % len(COLORS)]
                    colored_mask = np.zeros_like(img)
                    colored_mask[:, :, 0] = (mask > 0) * color[0]
                    colored_mask[:, :, 1] = (mask > 0) * color[1]
                    colored_mask[:, :, 2] = (mask > 0) * color[2]
                    img = cv2.addWeighted(img, 1.0, colored_mask, 0.4, 0)
                    
                    # Draw Label Center
                    M = cv2.moments((mask > 0).astype(np.uint8))
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        label_text = objects_registry.get(obj_id, "?")
                        cv2.putText(img, label_text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # 2. Draw Prompts
        if current_frame_idx in prompts_store:
            for obj_id, p_list in prompts_store[current_frame_idx].items():
                # Dim points not for current object?
                # or just draw them
                for p in p_list:
                    color = (0, 255, 0) if p[2] == 1 else (0, 0, 255)
                    cv2.circle(img, (p[0], p[1]), 5, color, -1)
                    if obj_id == current_obj_id:
                         cv2.circle(img, (p[0], p[1]), 7, (255, 255, 255), 1)

        # 3. Status Bar
        h, w = img.shape[:2]
        # Top Bar
        cv2.rectangle(img, (0, 0), (w, 50), (0, 0, 0), -1)
        cv2.putText(img, f"Frame: {current_frame_idx}/{total_frames} | Skip: {skip_step}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(img, f"Active Object: ID {current_obj_id} [{objects_registry.get(current_obj_id)}]", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Controls Help
        help_text = "[Space] Track+1 | [S] Export | [N] Propagate All | [Tab] New Obj | [K/L] Jump | [Del] Delete"
        cv2.putText(img, help_text, (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
        cv2.putText(img, help_text, (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'): break
        elif key == ord('l'): # Jump Forward
            current_frame_idx = min(total_frames - 1, current_frame_idx + skip_step)
        elif key == ord('k'): # Jump Backward
            current_frame_idx = max(0, current_frame_idx - skip_step)
        elif key == ord(' '): # Stepwise Track
            # Propagate 1 frame (Current -> Next)
            # We want to see the effect on the NEXT frame.
            # So start from current, step 2 (current + 1 more).
            # Actually, calculate for current and next.
            run_propagation(start_frame=current_frame_idx, max_steps=2)
            # Auto-advance selection to next frame for convenience?
            # User said "track the next frame", usually implies moving there.
            if current_frame_idx < total_frames - 1:
                current_frame_idx += 1
        elif key == ord('n'): # Propagate All
            run_propagation(start_frame=current_frame_idx)
        elif key == ord('s'):
            export_data()
        elif key == 9: # Tab
            create_new_object()
        elif key == 255 or key == 127 or key == 8: # Delete/Backspace (varies by OS)
            # Delete prompt for this obj on this frame?
            # Or Prompt to delete ENTIRE object?
            # User said "remove the label if we dont need it"
            # Let's verify intention.
            # Simple version: Clear prompts/masks for this object on this frame
            if current_frame_idx in prompts_store and current_obj_id in prompts_store[current_frame_idx]:
                 del prompts_store[current_frame_idx][current_obj_id]
            if current_frame_idx in cached_masks and current_obj_id in cached_masks[current_frame_idx]:
                 del cached_masks[current_frame_idx][current_obj_id]
            # Re-run inference to clear
            backend.reset_state() # Too destructive?
            # SAM 2 supports remove_object? 
            # Not easily exposed in our wrapper without re-init.
            # For now, just clearing viz.
            print(f"Cleared Object {current_obj_id} from Frame {current_frame_idx}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
