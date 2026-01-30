
import cv2
from run_yolo import process_video
import os

def test_integration():
    model_path = "best.pt"
    video_path = "Construction_Safety_Hazard_CCTV_Video.mp4"
    output_path = "test_output.mp4"
    
    # Mock cv2.VideoCapture to only return a few frames or just run on real video for short time?
    # run_yolo process_video runs until end of video. 
    # Be careful not to run for too long if video is long.
    # The current run_yolo implementation doesn't have a max_frames argument.
    
    # I'll monkeypatch cv2.VideoCapture to stop early.
    original_VideoCapture = cv2.VideoCapture
    
    class MockCap:
        def __init__(self, path):
            self.cap = original_VideoCapture(path)
            self.count = 0
            self.limit = 10 
            
        def isOpened(self):
            return self.cap.isOpened()
            
        def read(self):
            if self.count >= self.limit:
                return False, None
            self.count += 1
            return self.cap.read()
            
        def get(self, prop):
            return self.cap.get(prop)
            
        def release(self):
            self.cap.release()
            
    cv2.VideoCapture = MockCap
    
    try:
        if not os.path.exists(model_path):
            # Fallback to yolov8n.pt if best.pt missing
            model_path = "yolov8n.pt"
            
        print(f"Testing with model: {model_path}")
        process_video(model_path, video_path, output_path, tracker="botsort.yaml", conf=0.25)
        print("Integration test passed.")
        return 0
    except Exception as e:
        print(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
if __name__ == "__main__":
    import sys
    sys.exit(test_integration())
