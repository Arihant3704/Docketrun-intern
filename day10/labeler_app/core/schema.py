from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
import numpy as np

@dataclass
class ObjectMeta:
    """Metadata for a single object class/instance."""
    obj_id: int
    class_name: str
    color: Tuple[int, int, int] # RGB
    created_at_frame: int = 0
    visible: bool = True
    
@dataclass
class FrameAnnotation:
    """Annotations for a single frame."""
    frame_idx: int
    # Mapping of obj_id -> Mask (binary numpy array or compressed RLE)
    masks: Dict[int, Any] = field(default_factory=dict) 
    # Mapping of obj_id -> BBox [x1, y1, x2, y2]
    bboxes: Dict[int, List[float]] = field(default_factory=dict)
    # List of SAM points: (obj_id, x, y, label)
    points: List[Tuple[int, float, float, int]] = field(default_factory=list)

@dataclass
class ProjectManifest:
    """Project configuration and metadata."""
    name: str
    video_path: str
    created_at: str
    last_modified: str
    classes: List[str]
    version: str = "1.0.0"
    
@dataclass
class AppState:
    """Runtime application state."""
    current_frame: int = 0
    current_obj_id: int = 1
    selected_tool: str = "detect" # detect, track, edit
    is_propagating: bool = False
    zoom_level: float = 1.0
    pan_offset: Tuple[int, int] = (0, 0)
