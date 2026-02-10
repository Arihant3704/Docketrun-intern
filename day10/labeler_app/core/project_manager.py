import os
import json
import shutil
import glob
from typing import Optional
from PIL import Image
import numpy as np
from ..utils.logger import app_logger

class ProjectManager:
    """Handles loading, saving, and crash recovery of projects."""
    
    def __init__(self, projects_root="projects"):
        self.projects_root = projects_root
        os.makedirs(self.projects_root, exist_ok=True)
        self.current_project_path = None
        
    def create_project(self, name: str, video_path: str, classes: list):
        project_dir = os.path.join(self.projects_root, name)
        if os.path.exists(project_dir):
            raise FileExistsError(f"Project '{name}' already exists.")
            
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, "images"))
        os.makedirs(os.path.join(project_dir, "masks")) # Cache
        
        manifest = {
            "name": name,
            "video_path": video_path,
            "classes": classes,
            "version": "1.0.0"
        }
        
        with open(os.path.join(project_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)
            
        self.current_project_path = project_dir
        app_logger.info(f"Created project: {name}")
        return project_dir

    def save_project(self, annotation_manager):
        """Atomic save of annotations."""
        if not self.current_project_path: return
        
        # Serialize annotations
        data = {
            "objects": [obj.__dict__ for obj in annotation_manager.objects.values()],
            "annotations": {} # Simplified serializable format
        }
        
        masks_dir = os.path.join(self.current_project_path, "masks")
        if not os.path.exists(masks_dir): os.makedirs(masks_dir)

        # Convert annotations to serializable dict
        for frame, ann in annotation_manager.annotations.items():
             data["annotations"][frame] = {
                 "bbox": ann.bboxes
             }
             
             # Save Masks as PNG
             for obj_id, mask in ann.masks.items():
                 if mask is None: continue
                 
                 # clean mask
                 m = mask > 0
                 # Squeeze if needed (robustness)
                 if m.ndim > 2: m = m.squeeze()
                 if m.ndim != 2: continue
                 
                 try:
                     filename = f"{int(frame):05d}_{int(obj_id)}.png"
                     filepath = os.path.join(masks_dir, filename)
                     
                     # 0 or 255
                     img = Image.fromarray((m * 255).astype(np.uint8))
                     img.save(filepath)
                 except Exception as e:
                     app_logger.error(f"Failed to save mask {frame}_{obj_id}: {e}")

             
        save_path = os.path.join(self.current_project_path, "annotations.json")
        temp_path = save_path + ".tmp"
        
        with open(temp_path, "w") as f:
            json.dump(data, f)
            
        # Atomic rename
        shutil.move(temp_path, save_path)
        app_logger.info("Project saved successfully.")
        
    def load_project(self, project_dir: str):
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"Project not found: {project_dir}")
            
        manifest_path = os.path.join(project_dir, "manifest.json")
        if not os.path.exists(manifest_path):
             raise FileNotFoundError(f"Invalid project: manifest.json missing in {project_dir}")
             
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        self.current_project_path = project_dir
        
        # Load Annotations JSON
        annotations_path = os.path.join(project_dir, "annotations.json")
        data = {"objects": [], "annotations": {}}
        
        if os.path.exists(annotations_path):
            with open(annotations_path, "r") as f:
                data = json.load(f)
                
        # Load Masks from PNGs
        masks_dir = os.path.join(project_dir, "masks")
        loaded_masks = {} # (frame_idx) -> {obj_id: mask_np}
        
        if os.path.exists(masks_dir):
            for filename in os.listdir(masks_dir):
                if not filename.endswith(".png"): continue
                try:
                    # Parse filename: 00123_1.png
                    parts = filename[:-4].split("_")
                    if len(parts) != 2: continue
                    
                    frame_idx = int(parts[0])
                    obj_id = int(parts[1])
                    
                    filepath = os.path.join(masks_dir, filename)
                    img = Image.open(filepath).convert("L") # Grayscale
                    # Any pixel > 128 is True
                    mask = np.array(img) > 128
                    
                    if frame_idx not in loaded_masks: loaded_masks[frame_idx] = {}
                    loaded_masks[frame_idx][obj_id] = mask
                    
                except Exception as e:
                    app_logger.warning(f"Failed to load mask {filename}: {e}")
                
        return manifest, data, loaded_masks

    def check_for_recovery(self):
        """Checks for temp files indicative of a crash."""
        if not self.current_project_path: return False
        temps = glob.glob(os.path.join(self.current_project_path, "*.tmp"))
        if temps:
            app_logger.warning(f"Found {len(temps)} recovery files. Previous save might have crashed.")
            return True
        return False
