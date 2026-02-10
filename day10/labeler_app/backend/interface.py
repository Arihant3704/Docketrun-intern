from abc import ABC, abstractmethod
from typing import Generator

class SegmentationModel(ABC):
    """Abstract interface for segmentation backends."""
    
    @abstractmethod
    def set_video(self, video_path: str):
        pass
        
    @abstractmethod
    def add_point(self, frame_idx: int, points, labels, obj_id: int):
        pass
        
    @abstractmethod
    def propagate(self, start_frame: int, max_frames: int) -> Generator:
        pass
        
    @abstractmethod
    def get_frame(self, frame_idx: int) -> str:
        pass
