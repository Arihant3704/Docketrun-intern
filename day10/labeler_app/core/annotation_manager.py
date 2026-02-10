import copy
from typing import Dict, List, Optional
from .schema import FrameAnnotation, ObjectMeta
from ..utils.logger import app_logger

class AnnotationManager:
    """Central state manager for annotations with Undo/Redo."""
    
    def __init__(self):
        self.annotations: Dict[int, FrameAnnotation] = {}
        self.objects: Dict[int, ObjectMeta] = {}
        self.undo_stack: List[Dict] = []
        self.redo_stack: List[Dict] = []
        self.max_history = 20
        
    def _save_state(self):
        """Snapshots the current state for undo."""
        state = {
            "annotations": copy.deepcopy(self.annotations),
            "objects": copy.deepcopy(self.objects)
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        self.redo_stack.clear()
        
    def undo(self):
        if not self.undo_stack:
            return False
        
        # Save current state to redo
        current_state = {
            "annotations": copy.deepcopy(self.annotations),
            "objects": copy.deepcopy(self.objects)
        }
        self.redo_stack.append(current_state)
        
        # Restore previous
        prev_state = self.undo_stack.pop()
        self.annotations = prev_state["annotations"]
        self.objects = prev_state["objects"]
        app_logger.info("Undo performed.")
        return True
        
    def redo(self):
        if not self.redo_stack:
            return False
            
        # Save current to undo
        current_state = {
             "annotations": copy.deepcopy(self.annotations),
             "objects": copy.deepcopy(self.objects)
        }
        self.undo_stack.append(current_state)
        
        # Restore next
        next_state = self.redo_stack.pop()
        self.annotations = next_state["annotations"]
        self.objects = next_state["objects"]
        app_logger.info("Redo performed.")
        return True

    # --- Mutators (Must call _save_state) ---
    
    def add_object(self, obj_id: int, name: str, color: tuple):
        self._save_state()
        self.objects[obj_id] = ObjectMeta(obj_id, name, color)

    def rename_object(self, obj_id: int, new_name: str):
        self._save_state()
        if obj_id in self.objects:
            self.objects[obj_id].class_name = new_name
        
    def update_mask(self, frame_idx: int, obj_id: int, mask):
        self._save_state()
        if frame_idx not in self.annotations:
            self.annotations[frame_idx] = FrameAnnotation(frame_idx)
        self.annotations[frame_idx].masks[obj_id] = mask
        
    def delete_object(self, obj_id: int):
        self._save_state()
        if obj_id in self.objects:
            del self.objects[obj_id]
        
        # Remove annotations
        for frame_ann in self.annotations.values():
            if obj_id in frame_ann.masks:
                del frame_ann.masks[obj_id]
                
    def get_annotation(self, frame_idx: int) -> Optional[FrameAnnotation]:
        return self.annotations.get(frame_idx)

    def delete_mask(self, frame_idx: int, obj_id: int):
        """Removes mask for obj_id only on frame_idx."""
        self._save_state()
        if frame_idx in self.annotations:
            if obj_id in self.annotations[frame_idx].masks:
                del self.annotations[frame_idx].masks[obj_id]

    def reassign_mask(self, frame_idx: int, old_obj_id: int, new_name: str):
        """Moves mask from old_obj_id to a new/existing object with new_name on frame_idx."""
        self._save_state()
        if frame_idx not in self.annotations: return
        
        # Get mask
        mask = self.annotations[frame_idx].masks.get(old_obj_id)
        if mask is None: return
        
        # Find or Create Target Object ID
        target_obj_id = None
        for obj in self.objects.values():
            if obj.class_name == new_name:
                target_obj_id = obj.obj_id
                break
        
        if target_obj_id is None:
            target_obj_id = max(self.objects.keys(), default=0) + 1
            # Auto-assign color?
            import random
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.objects[target_obj_id] = ObjectMeta(target_obj_id, new_name, color)
            
        # Move mask
        self.annotations[frame_idx].masks[target_obj_id] = mask
        del self.annotations[frame_idx].masks[old_obj_id]
        
        return target_obj_id
