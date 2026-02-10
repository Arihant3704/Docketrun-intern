from typing import Dict, List
from .schema import FrameAnnotation
from ..utils.logger import app_logger

class Validator:
    """Validates dataset integrity before export."""
    
    @staticmethod
    def validate_annotations(annotations: Dict[int, FrameAnnotation], max_frames: int) -> List[str]:
        errors = []
        for frame_idx, ann in annotations.items():
            # Check bounds
            if frame_idx < 0 or frame_idx >= max_frames:
                errors.append(f"Frame {frame_idx} is out of bounds (0-{max_frames-1})")
                
            # Check objects
            for obj_id, mask in ann.masks.items():
                if mask is None:
                     errors.append(f"Frame {frame_idx}: Object {obj_id} has None mask")
                elif hasattr(mask, 'max') and mask.max() == 0:
                     app_logger.warning(f"Frame {frame_idx}: Object {obj_id} has empty mask")
        
        return errors
    
    @staticmethod
    def validate_project_structure(project_path: str) -> bool:
        # TODO: Check if directories exist
        return True
