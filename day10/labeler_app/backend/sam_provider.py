import os
import torch
import numpy as np
import cv2
import glob
from sam2.build_sam import build_sam2_video_predictor
from .interface import SegmentationModel
from ..utils.logger import app_logger

class SAM2Provider(SegmentationModel):
    def __init__(self, checkpoint_path, config_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            # auto-select bfloat16 or float16
            if torch.cuda.get_device_capability()[0] >= 8:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                
        app_logger.info(f"Loading SAM 2 on {self.device}...")
        try:
             self.predictor = build_sam2_video_predictor(config_path, checkpoint_path, device=self.device)
        except Exception as e:
             app_logger.error(f"Failed to load SAM 2: {e}")
             raise
             
        self.inference_state = None
        self.video_path = None
        self.frame_paths = []

    def set_video(self, video_path: str, cache_dir: str = None):
        self.video_path = video_path
        app_logger.info(f"Initializing video: {video_path}")
        
        # 1. Initialize SAM 2 State
        self.inference_state = self.predictor.init_state(video_path=video_path)
        
        # 2. Robust Frame Management
        # Instead of relying on internal cache, we expect 'cache_dir' to be provided
        # matching our project structure.
        self.frame_paths = []
        if cache_dir:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
                
            # Check if frames exist, if not extract
            existing_frames = sorted(glob.glob(os.path.join(cache_dir, "*.jpg")))
            
            if not existing_frames:
                app_logger.info(f"Extracting frames to {cache_dir}...")
                cap = cv2.VideoCapture(video_path)
                idx = 0
                while True:
                    ret, frame = cap.read()
                    if not ret: break
                    frame_path = os.path.join(cache_dir, f"{idx:06d}.jpg")
                    cv2.imwrite(frame_path, frame)
                    self.frame_paths.append(frame_path)
                    idx += 1
                cap.release()
            else:
                self.frame_paths = existing_frames
                
            app_logger.info(f"Loaded {len(self.frame_paths)} frames.")
        else:
            # Fallback (Legacy/Test): Try to find internal cache or fail
            app_logger.warning("No cache_dir provided. Trying manual extraction to temp...")
             # ... (Skipped for now, Controller should provide cache_dir)

    def get_frame(self, frame_idx: int) -> str:
        if 0 <= frame_idx < len(self.frame_paths):
            return self.frame_paths[frame_idx]
        return None

    def add_point(self, frame_idx: int, points, labels, obj_id: int):
        """points: Nx2 float32, labels: N int32 (1=pos, 0=neg)"""
        if not self.inference_state: return None
        
        _, out_obj_ids, out_mask_logits = self.predictor.add_new_points_or_box(
            inference_state=self.inference_state,
            frame_idx=frame_idx,
            obj_id=obj_id,
            points=points,
            labels=labels,
        )
        
        # Extract the mask for the current object
        for i, out_obj_id in enumerate(out_obj_ids):
            if out_obj_id == obj_id:
                mask = (out_mask_logits[i] > 0.0).cpu().numpy().squeeze()
                return mask
        return None

    def propagate(self, start_frame: int, max_frames: int):
        """Yields (frame_idx, obj_ids, masks)"""
        if not self.inference_state: return
        
        # Hack: self.predictor.propagate_in_video currently runs from start to end
        # We need to manually control the loop or reset
        # For this implementation, we rely on the standard generator
        
        count = 0
        generator = self.predictor.propagate_in_video(
            self.inference_state,
            start_frame_idx=start_frame,
            max_frame_num_to_track=max_frames
        )
        
        while True:
            try:
                out_frame_idx, out_obj_ids, out_mask_logits = next(generator)
            except StopIteration:
                break
            except Exception as e:
                app_logger.error(f"SAM 2 Internal Error during propagation: {e}")
                # If the predictor crashes, we probably can't continue safely, but we yield nothing and break
                break

            try:
                 # Ensure out_obj_ids is list
                 if isinstance(out_obj_ids, (int, np.integer)):
                     out_obj_ids = [out_obj_ids]
                 elif isinstance(out_obj_ids, np.ndarray) and out_obj_ids.ndim == 0:
                     out_obj_ids = [out_obj_ids.item()]
                     
                 # Process Masks
                 try:
                     masks_np = (out_mask_logits > 0.0).cpu().numpy()
                 except AttributeError:
                     masks_np = np.array(out_mask_logits > 0.0)

                 if masks_np.ndim == 0:
                     masks_np = np.expand_dims(masks_np, axis=0)

                 cleaned_masks = []
                 for i in range(len(out_obj_ids)):
                     if i >= masks_np.shape[0]: break
                     
                     stats = masks_np[i]
                     if stats.ndim == 3 and stats.shape[0] == 1:
                         cleaned_masks.append(stats.squeeze(0))
                     elif stats.ndim == 2:
                         cleaned_masks.append(stats)
                     else:
                         sq = stats.squeeze()
                         if sq.ndim == 2:
                             cleaned_masks.append(sq)
                         else:
                             pass
                             
                 yield out_frame_idx, out_obj_ids, cleaned_masks
                 
            except Exception as e:
                 app_logger.error(f"Error processing frame output: {e}")
                 continue
                 
            count += 1
            if max_frames and count >= max_frames:
                break
                 
    def reset_state(self):
        if self.inference_state:
            self.predictor.reset_state(self.inference_state)
