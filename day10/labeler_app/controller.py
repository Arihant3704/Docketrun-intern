import os
from .core.annotation_manager import AnnotationManager
from .core.project_manager import ProjectManager
from .core.task_manager import TaskManager
from .utils.logger import app_logger
from .backend.sam_provider import SAM2Provider
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class AppController:
    """The Brain: Mediates between UI and Core/Backend."""
    
    def __init__(self):
        self.am = AnnotationManager()
        self.pm = ProjectManager()
        self.tm = TaskManager()
        self.backend = None 
        
        # State
        self.current_frame_idx = 0
        self.total_frames = 0
        self.current_mode = "detect" # detect, track, edit
        self.active_obj_id = 1
        self.is_playing = False
        
        # Hooks
        self.ui = None # Reference to MainWindow

    def bind_ui(self, main_window):
        self.ui = main_window

    def initialize_project(self, name, video_path, classes):
        try:
            self.pm.create_project(name, video_path, classes)
            self._init_backend_and_state(video_path, classes)
            app_logger.info("Project initialized.")
        except FileExistsError:
            app_logger.error(f"Project '{name}' exists.")
            if self.ui: self.ui.update_status(f"Error: Project '{name}' already exists. Use Open Project.")
        except Exception as e:
            app_logger.error(f"Init failed: {e}")
            if self.ui: self.ui.update_status(f"Error: {e}")

    def open_project(self, project_dir):
        try:
            manifest, data, loaded_masks = self.pm.load_project(project_dir)
            video_path = manifest["video_path"]
            classes = manifest["classes"]
            
            self._init_backend_and_state(video_path, classes)
            
            # Restore state
            # 1. Objects
            self.am.objects.clear()
            for obj_dict in data.get("objects", []):
                # Ensure tuple color
                if "color" in obj_dict: obj_dict["color"] = tuple(obj_dict["color"]) 
                # Reconstruct ObjectMeta (simple dict update for now)
                from .core.schema import ObjectMeta
                obj = ObjectMeta(**obj_dict)
                self.am.objects[obj.obj_id] = obj
                
            # 2. Annotations (Images/Masks)
            self.am.annotations.clear()
            
            for frame_idx, masks_dict in loaded_masks.items():
                for obj_id, mask in masks_dict.items():
                    # This will create FrameAnnotation if needed and update bbox automatically
                    self.am.update_mask(frame_idx, obj_id, mask)
            
            self.load_frame(0)
            app_logger.info(f"Project loaded: {project_dir}")
            if self.ui: self.ui.update_status(f"Project loaded: {manifest['name']}")
            
        except Exception as e:
            app_logger.error(f"Open failed: {e}")
            if self.ui: self.ui.update_status(f"Error: {e}")

    def _init_backend_and_state(self, video_path, classes):
        # Helper to avoid duplication
        # Init Backend
        chkpt = "sam2_repo/checkpoints/sam2.1_hiera_base_plus.pt"
        cfg = "configs/sam2.1/sam2.1_hiera_b+.yaml"
        
        self.backend = SAM2Provider(chkpt, cfg)
        
        # Determine project images path
        images_dir = None
        if self.pm.current_project_path:
            images_dir = os.path.join(self.pm.current_project_path, "images")
            
        self.backend.set_video(video_path, cache_dir=images_dir)
        
        self.total_frames = len(self.backend.frame_paths)
        if self.ui:
            self.ui.timeline.set_total_frames(self.total_frames)
            
        # Setup Initial State (Default object if empty)
        if not self.am.objects:
             self.am.add_object(1, classes[0], (0, 255, 0))
        
        self.load_frame(0)

    def load_frame(self, frame_idx):
        if not self.backend: return
        self.current_frame_idx = frame_idx
        
        # Load Image
        img_path = self.backend.get_frame(frame_idx)
        if img_path:
            pil_img = Image.open(img_path).convert("RGBA")
            w, h = pil_img.size
            
            # Overlay masks from AM
            annotation = self.am.get_annotation(frame_idx)
            if annotation:
                # Create a blank overlay layer
                overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                overlay_np = np.zeros((h, w, 4), dtype=np.uint8)
                
                for obj_id, mask in annotation.masks.items():
                    if mask is None: continue
                    # Ensure mask is binary
                    if hasattr(mask, 'max') and mask.max() > 0:
                        obj_meta = self.am.objects.get(obj_id)
                        color = obj_meta.color if obj_meta else (255, 0, 0)
                        
                        # Robust shape handling
                        m = mask > 0
                        
                        # Fix dim issues (1, H, W) -> (H, W)
                        if m.ndim > 2 and m.shape[0] == 1:
                            m = m.squeeze(0)
                        
                        # Safety check
                        if m.shape != (h, w):
                            # Skip if shape mismatch to prevent crash
                            continue
                            
                        overlay_np[m] = [*color, 128] # RGB + Alpha=128
                        
                # Convert numpy overlay to PIL
                mask_layer = Image.fromarray(overlay_np, "RGBA")
                pil_img = Image.alpha_composite(pil_img, mask_layer)
                
                # Draw Labels
                draw = ImageDraw.Draw(pil_img)
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except IOError:
                    font = ImageFont.load_default()
                    
                for obj_id, mask in annotation.masks.items():
                    if mask is None: continue
                    if hasattr(mask, 'max') and mask.max() > 0:
                        m = mask > 0
                        if m.ndim > 2: m = m.squeeze()
                        if m.ndim != 2: continue
                        
                        # Find top-left of mask
                        ys, xs = np.where(m)
                        if len(xs) > 0 and len(ys) > 0:
                            x, y = xs.min(), ys.min()
                            obj_meta = self.am.objects.get(obj_id)
                            if obj_meta:
                                text = f"{obj_meta.class_name} {obj_id}"
                                # Draw background rectangle for readability
                                bbox = draw.textbbox((x, y), text, font=font)
                                draw.rectangle(bbox, fill=(0, 0, 0, 128))
                                draw.text((x, y), text, fill=(255, 255, 255), font=font)

            if self.ui:
                self.ui.canvas.set_image(pil_img)
                self.ui.timeline.set_current_frame(frame_idx)
                # self.ui.toolbox.update_object_list(self.am.objects) # Optim: Don't update every frame

    def get_object_at(self, x, y):
        """Returns object ID at image coordinates (x, y) or None."""
        annotation = self.am.get_annotation(self.current_frame_idx)
        if not annotation: return None
        
        # Check in reverse order (topmost first if overlapping?) 
        # Actually random/dict order. Improvements might needed for z-order.
        for obj_id, mask in annotation.masks.items():
             if mask is None: continue
             # Check bounds first
             if 0 <= y < mask.shape[0] and 0 <= x < mask.shape[1]:
                 if mask[y, x] > 0:
                     return obj_id
        return None

    def rename_object(self, obj_id, new_name):
        self.am.rename_object(obj_id, new_name)
        self.load_frame(self.current_frame_idx)
        if self.ui:
             self.ui.toolbox.update_object_list(self.am.objects)

    def delete_object_global(self, obj_id):
        self.am.delete_object(obj_id)
        self.load_frame(self.current_frame_idx)
        if self.ui:
            self.ui.toolbox.update_object_list(self.am.objects)

    def delete_mask_on_frame(self, obj_id):
        self.am.delete_mask(self.current_frame_idx, obj_id)
        self.load_frame(self.current_frame_idx)

    def reassign_mask_on_frame(self, obj_id, new_name):
        new_id = self.am.reassign_mask(self.current_frame_idx, obj_id, new_name)
        self.load_frame(self.current_frame_idx)
        if self.ui:
            self.ui.toolbox.update_object_list(self.am.objects)
        return new_id

    def handle_canvas_click(self, x, y, button, width, height):
        """Handle click on canvas. Coords are screen relative, need scaling."""
        if not self.backend: return
        
        # Scale coords based on zoom/pan (logic usually in Canvas, receiving generic 0-1 or image-relative here?)
        # Assuming Arguments x,y are IMAGE RELATIVE pixels
        
        if self.current_mode == "detect":
            label = 1 if button == 1 else 0 # Left=Pos, Right=Neg
            
            # Backend Add Point
            points = np.array([[x, y]], dtype=np.float32)
            labels = np.array([label], dtype=np.int32)
            
            try:
                mask = self.backend.add_point(self.current_frame_idx, points, labels, self.active_obj_id)
                if mask is not None:
                    self.am.update_mask(self.current_frame_idx, self.active_obj_id, mask)
                    self.load_frame(self.current_frame_idx) # Refresh
            except Exception as e:
                app_logger.error(f"Inference Error: {e}")

    def set_mode(self, mode):
        self.current_mode = mode
        if self.ui: self.ui.update_status(f"Mode: {mode}")

    def change_frame(self, delta):
        new_frame = max(0, min(self.total_frames - 1, self.current_frame_idx + delta))
        self.load_frame(new_frame)
        
    def propagate(self, max_frames=None):
        if not self.backend: return
        
        def task_func(stop_event):
            # Run propagation
            gen = self.backend.propagate(self.current_frame_idx, max_frames=max_frames) # User defined or All
            for f_idx, obj_ids, masks in gen:
                if stop_event.is_set(): break
                # Update AM
                for i, obj in enumerate(obj_ids):
                    self.am.update_mask(f_idx, obj, masks[i])
        
        self.tm.start_task(task_func, on_complete=lambda: self.load_frame(self.current_frame_idx))

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.ui:
            self.ui.timeline.update_play_button(self.is_playing)
            
        if self.is_playing:
            self._playback_loop()
            
    def _playback_loop(self):
        if not self.is_playing: return
        
        if self.current_frame_idx < self.total_frames - 1:
            self.load_frame(self.current_frame_idx + 1)
            if self.ui:
                self.ui.after(30, self._playback_loop)
        else:
            self.is_playing = False
            if self.ui:
                self.ui.timeline.update_play_button(False)

    def stop_propagation(self):
        self.tm.stop_current_task()
        if self.ui: self.ui.update_status("Propagation stopped.")
    
    def save(self):
        self.tm.start_task(
            target=lambda stop_evt: self.pm.save_project(self.am),
            on_complete=lambda: self.ui.update_status("Saved.") if self.ui else None
        )

    def undo(self):
        if self.am.undo():
            self.load_frame(self.current_frame_idx)
            self.ui.toolbox.update_object_list(self.am.objects)
            
    def redo(self):
        if self.am.redo():
            self.load_frame(self.current_frame_idx)
            self.ui.toolbox.update_object_list(self.am.objects)

    def export(self):
        from .backend.exporter import Exporter
        if self.pm.current_project_path and self.backend:
             self.ui.update_status("Exporting...")
             
             def run_export(stop_evt):
                 return Exporter.export_yolo(self.pm.current_project_path, self.am, dict(enumerate(self.backend.frame_paths)))
                 
             def on_done(result):
                 if not result: return 
                 path, count = result
                 msg = f"Exported {count} frames to {path}"
                 if count == 0:
                     msg += "\n\n(No masks were found! Did you propagate/track objects?)"
                 
                 from tkinter import messagebox
                 messagebox.showinfo("Export Complete", msg)
                 self.ui.update_status(f"Exported {count} frames.")

             self.tm.start_task(target=run_export, on_complete=on_done)
