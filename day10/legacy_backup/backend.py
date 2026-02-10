import os
import cv2
import torch
import numpy as np
import shutil
import sys
# Add sam2_repo to path to ensure import works if pip install -e failed or env issue
sys.path.append(os.path.join(os.path.dirname(__file__), "sam2_repo"))

from sam2.build_sam import build_sam2_video_predictor

class SAM2Backend:
    # Config path should be relative for Hydra (pkg://sam2)
    # We use the standard SAM 2.1 config name
    def __init__(self, model_cfg="configs/sam2.1/sam2.1_hiera_b+.yaml", checkpoint="sam2_repo/checkpoints/sam2.1_hiera_base_plus.pt"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cpu":
            print("Warning: Running on CPU. SAM 2 will be slow.")

        # Checkpoint should be absolute or correct relative to CWD
        if not os.path.exists(checkpoint):
             # Try absolute path based on file location
             possible_ckpt = os.path.join(os.path.dirname(__file__), checkpoint)
             if os.path.exists(possible_ckpt):
                 checkpoint = possible_ckpt
             else:
                 print(f"Checkpoint {checkpoint} not found!")

        print(f"Loading SAM 2 from {checkpoint} with config {model_cfg}...")
        try:
            self.predictor = build_sam2_video_predictor(model_cfg, checkpoint, device=self.device)
            self.inference_state = None
        except Exception as e:
            print(f"Error building SAM 2 predictor: {e}")
            raise e
        self.video_path = None
        self.frame_dir = None
        self.frame_names = []
        
    def set_video(self, video_path, cache_dir="video_frames_cache"):
        """
        Extracts frames from video and initializes SAM 2 state.
        """
        self.video_path = video_path
        self.frame_dir = cache_dir
        
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        os.makedirs(cache_dir, exist_ok=True)
        
        print(f"Extracting frames from {video_path} to {cache_dir}...")
        cap = cv2.VideoCapture(video_path)
        frame_idx = 0
        self.frame_names = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_name = f"{frame_idx:05d}.jpg"
            cv2.imwrite(os.path.join(cache_dir, frame_name), frame)
            self.frame_names.append(frame_name)
            frame_idx += 1
        cap.release()
        print(f"Extracted {len(self.frame_names)} frames.")
        
        # Initialize SAM 2 state
        self.inference_state = self.predictor.init_state(video_path=cache_dir)
        self.reset_state()
        
    def reset_state(self):
        self.predictor.reset_state(self.inference_state)

    def add_point(self, frame_idx, points, labels, obj_id=1):
        """
        Interact with the model on a specific frame.
        points: List of [x, y]
        labels: List of 0/1 (0=negative, 1=positive)
        """
        if self.inference_state is None:
            raise ValueError("Video not set. Call set_video() first.")
            
        frame_idx, out_obj_ids, out_mask_logits = self.predictor.add_new_points_or_box(
            inference_state=self.inference_state,
            frame_idx=frame_idx,
            obj_id=obj_id,
            points=points,
            labels=labels,
        )
        
        # Return the mask for visualization
        # MASK shape is (N_obj, H, W)
        mask = (out_mask_logits[0] > 0.0).cpu().numpy().squeeze()
        return mask

    def propagate(self, start_frame_idx=0, max_frames=None):
        """
        Propagate masks across the video.
        Returns a generator of (frame_idx, obj_ids, mask_logits).
        """
        if self.inference_state is None:
            return
            
        count = 0
        for out_frame_idx, out_obj_ids, out_mask_logits in self.predictor.propagate_in_video(self.inference_state, start_frame_idx=start_frame_idx):
            yield out_frame_idx, out_obj_ids, (out_mask_logits > 0.0).cpu().numpy()
            count += 1
            if max_frames is not None and count >= max_frames:
                break

    def get_frame(self, frame_idx):
        if 0 <= frame_idx < len(self.frame_names):
            return os.path.join(self.frame_dir, self.frame_names[frame_idx])
        return None
    
    def get_num_frames(self):
        return len(self.frame_names)

