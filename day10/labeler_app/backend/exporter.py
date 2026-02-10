import os
import shutil
import cv2
import numpy as np
from ..core.annotation_manager import AnnotationManager
from ..utils.logger import app_logger

class Exporter:
    """Exports project data to standard formats (YOLO)."""
    
    @staticmethod
    def export_yolo(project_path: str, ann_manager: AnnotationManager, frame_paths: dict):
        export_dir = os.path.join(project_path, "export_yolo")
        images_dir = os.path.join(export_dir, "images")
        labels_dir = os.path.join(export_dir, "labels")
        
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        
        # Create data.yaml
        classes = sorted(list(set(obj.class_name for obj in ann_manager.objects.values())))
        class_map = {name: i for i, name in enumerate(classes)}
        
        with open(os.path.join(export_dir, "data.yaml"), "w") as f:
            f.write(f"names: {classes}\n")
            f.write(f"path: {export_dir}\n")
            f.write("train: images\nval: images\n")
            
        count = 0
        for frame_idx, frame_ann in ann_manager.annotations.items():
            if not frame_ann.masks:
                # app_logger.debug(f"Skipping frame {frame_idx}: No masks found.")
                continue
            
            src_img = frame_paths.get(frame_idx)
            if not src_img or not os.path.exists(src_img):
                 app_logger.warning(f"Skipping frame {frame_idx}: Image not found at {src_img}")
                 continue
            
            # Copy image
            img_name = f"{frame_idx:06d}.jpg"
            shutil.copy(src_img, os.path.join(images_dir, img_name))
            
            # Write labels
            label_lines = []
            img = cv2.imread(src_img)
            h, w = img.shape[:2]
            
            for obj_id, mask in frame_ann.masks.items():
                obj_meta = ann_manager.objects.get(obj_id)
                if not obj_meta: continue
                
                cls_idx = class_map.get(obj_meta.class_name, 0)
                
                # Mask to Polygon
                contours, _ = cv2.findContours((mask > 0).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    if len(cnt) < 3: continue
                    norm_pts = cnt.reshape(-1, 2) / [w, h]
                    flat_pts = " ".join([f"{p[0]:.6f} {p[1]:.6f}" for p in norm_pts])
                    label_lines.append(f"{cls_idx} {flat_pts}\n")
                    
            if label_lines:
                with open(os.path.join(labels_dir, img_name.replace(".jpg", ".txt")), "w") as f:
                    f.writelines(label_lines)
                count += 1
                
        if count == 0:
            app_logger.warning("Exported 0 frames. Check if masks exist.")
            return export_dir, 0
            
        app_logger.info(f"Exported {count} frames to YOLO format at {export_dir}")
        return export_dir, count
