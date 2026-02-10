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

    # --- Helper Functions (Defines early to avoid NameErrors) ---
    def run_propagation(start_frame, max_steps=None):
        print(f"Propagating from frame {start_frame} (Max steps: {max_steps})...")
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
                # masks shape check
                if masks.ndim == 4: masks = masks.squeeze(1)
                
                # Check if we have valid object IDs
                if len(obj_ids) > 0:
                     for i, obj_id in enumerate(obj_ids):
                        cached_masks[frame_idx][obj_id] = masks[i]
                count += 1
        except Exception as e:
            print(f"Prop Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if popup: popup.destroy()
        print(f"Propagated {count} frames.")
        return count

    def create_new_object():
        nonlocal current_obj_id
        root = tk.Tk()
        root.withdraw()
        new_name = simpledialog.askstring("New Object", "Enter Class Name (e.g., person):")
        if new_name:
            next_id = max(objects_registry.keys()) + 1
            objects_registry[next_id] = new_name
            current_obj_id = next_id
            print(f"Switched to New Object: ID {current_obj_id} ({new_name})")

    def export_data():
        if not cached_masks:
             messagebox.showwarning("Warning", "No masks generated. Run propagation first.")
             return
             
        base_dir = os.path.dirname(video_path)
        ds_name = list(objects_registry.values())[0] if len(objects_registry) == 1 else "mixed"
        export_dir = os.path.join(base_dir, f"{ds_name}_dataset") 
        images_dir = os.path.join(export_dir, "images")
        labels_dir = os.path.join(export_dir, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        
        unique_classes = sorted(list(set(objects_registry.values())))
        class_to_idx = {name: i for i, name in enumerate(unique_classes)}
        
        yaml_content = f"names: {unique_classes}\npath: {export_dir}\ntrain: images\nval: images\n"
        with open(os.path.join(export_dir, "data_hint.yaml"), "w") as f:
            f.write(yaml_content)
            
        count = 0
        for frame_idx, objs_dict in cached_masks.items():
            if not objs_dict: continue
            
            frame_path = backend.get_frame(frame_idx)
            if not frame_path: continue
            shutil.copy(frame_path, os.path.join(images_dir, os.path.basename(frame_path)))
            
            h, w = 0, 0
            lines = []
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
                        norm_points.extend([pt[0] / w, pt[1] / h])
                    lines.append(f"{class_idx} {' '.join(map(str, norm_points))}\n")
            
            if lines:
                label_path = os.path.join(labels_dir, os.path.basename(frame_path).replace(".jpg", ".txt"))
                with open(label_path, "w") as f:
                    f.writelines(lines)
                count += 1
                
        messagebox.showinfo("Export Complete", f"Saved {count} labeled frames.\nValid Classes: {unique_classes}")

    # --- Buttons Layout ---
    BUTTONS = [
        {"name": "Prev <", "rect": (10, 10, 80, 40), "action": "prev"},
        {"name": "Next >", "rect": (100, 10, 80, 40), "action": "next"},
        {"name": "Track (Space)", "rect": (190, 10, 130, 40), "action": "track"},
        {"name": "Save (S)", "rect": (330, 10, 80, 40), "action": "save"},
        {"name": "New Obj", "rect": (420, 10, 100, 40), "action": "new_obj"},
        {"name": "Delete", "rect": (530, 10, 80, 40), "action": "delete"},
    ]

    def draw_buttons(img):
        # Draw a top bar background
        cv2.rectangle(img, (0, 0), (img.shape[1], 60), (50, 50, 50), -1)
        
        for btn in BUTTONS:
            x, y, w, h = btn["rect"]
            # Hover effect could be added here if we tracked mouse move
            cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 100), -1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), 1)
            
            # Text centering
            text_size = cv2.getTextSize(btn["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + (h + text_size[1]) // 2
            cv2.putText(img, btn["name"], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def handle_button_click(x, y):
        for btn in BUTTONS:
            bx, by, bw, bh = btn["rect"]
            if bx <= x <= bx + bw and by <= y <= by + bh:
                return btn["action"]
        return None

    # Actions Wrappers
    def action_prev():
        nonlocal current_frame_idx
        if current_frame_idx > 0:
            current_frame_idx -= 1

    def action_next():
        nonlocal current_frame_idx
        if current_frame_idx < total_frames - 1:
            current_frame_idx += 1

    def action_track():
        nonlocal current_frame_idx
        run_propagation(start_frame=current_frame_idx, max_steps=2)
        if current_frame_idx < total_frames - 1:
             current_frame_idx += 1

    def action_delete():
        if current_frame_idx in prompts_store and current_obj_id in prompts_store[current_frame_idx]:
             del prompts_store[current_frame_idx][current_obj_id]
        if current_frame_idx in cached_masks and current_obj_id in cached_masks[current_frame_idx]:
             del cached_masks[current_frame_idx][current_obj_id]
        print(f"Cleared Object {current_obj_id} from Frame {current_frame_idx}")
        # Force re-render of inference if backend state needs reset?
        # For visualization, clearing cache is enough. Backend state usually additive.

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check Buttons first
            if y < 60: # Top bar area
                act = handle_button_click(x, y)
                if act:
                    if act == "prev": action_prev()
                    elif act == "next": action_next()
                    elif act == "track": action_track()
                    elif act == "save": export_data()
                    elif act == "new_obj": create_new_object()
                    elif act == "delete": action_delete()
                return # Don't add points if clicked on button

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

    # --- Helper Functions ---
    def run_propagation(start_frame, max_steps=None):
        print(f"Propagating from frame {start_frame} (Max steps: {max_steps})...")
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
                if masks.ndim == 4: masks = masks.squeeze(1)
                for i, obj_id in enumerate(obj_ids):
                    cached_masks[frame_idx][obj_id] = masks[i]
                count += 1
        except Exception as e:
            print(f"Prop Error: {e}")
        finally:
            if popup: popup.destroy()
        print(f"Propagated {count} frames.")
        return count

    def create_new_object():
        nonlocal current_obj_id
        root = tk.Tk()
        root.withdraw()
        new_name = simpledialog.askstring("New Object", "Enter Class Name (e.g., person):")
        if new_name:
            next_id = max(objects_registry.keys()) + 1
            objects_registry[next_id] = new_name
            current_obj_id = next_id
            print(f"Switched to New Object: ID {current_obj_id} ({new_name})")

    def export_data():
        if not cached_masks:
             messagebox.showwarning("Warning", "No masks generated. Run propagation first.")
             return
             
        base_dir = os.path.dirname(video_path)
        ds_name = list(objects_registry.values())[0] if len(objects_registry) == 1 else "mixed"
        export_dir = os.path.join(base_dir, f"{ds_name}_dataset") 
        images_dir = os.path.join(export_dir, "images")
        labels_dir = os.path.join(export_dir, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        
        unique_classes = sorted(list(set(objects_registry.values())))
        class_to_idx = {name: i for i, name in enumerate(unique_classes)}
        
        yaml_content = f"names: {unique_classes}\npath: {export_dir}\ntrain: images\nval: images\n"
        with open(os.path.join(export_dir, "data_hint.yaml"), "w") as f:
            f.write(yaml_content)
            
        count = 0
        for frame_idx, objs_dict in cached_masks.items():
            if not objs_dict: continue
            
            frame_path = backend.get_frame(frame_idx)
            if not frame_path: continue
            shutil.copy(frame_path, os.path.join(images_dir, os.path.basename(frame_path)))
            
            h, w = 0, 0
            lines = []
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
                        norm_points.extend([pt[0] / w, pt[1] / h])
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
                for p in p_list:
                    color = (0, 255, 0) if p[2] == 1 else (0, 0, 255)
                    cv2.circle(img, (p[0], p[1]), 5, color, -1)
                    if obj_id == current_obj_id:
                         cv2.circle(img, (p[0], p[1]), 7, (255, 255, 255), 1)

        # 3. Draw Buttons (Top Bar)
        draw_buttons(img)

        # 4. Status Info
        cv2.putText(img, f"Frame: {current_frame_idx}/{total_frames} | Obj: {current_obj_id} [{objects_registry.get(current_obj_id)}]", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'): break
        elif key == ord('l'): current_frame_idx = min(total_frames - 1, current_frame_idx + skip_step)
        elif key == ord('k'): current_frame_idx = max(0, current_frame_idx - skip_step)
        elif key == ord(' '): action_track()
        elif key == ord('n'): action_next()
        elif key == ord('p'): action_prev()
        elif key == ord('s'): export_data()
        elif key == 9: create_new_object()
        elif key == 127 or key == 8: # Backspace/Delete (AVOID 255/NoKey)
            action_delete()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
