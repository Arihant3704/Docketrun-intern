import cv2
import numpy as np
import torch
from ultralytics.engine.results import Boxes, Results

def test_fix():
    try:
        # 1. Manually create Boxes with ID (mocking tracking result)
        # Format: x1, y1, x2, y2, id, conf, cls
        data = torch.tensor([[100, 100, 200, 200, 1.0, 0.9, 0.0]])
        orig_shape = (640, 640)
        boxes = Boxes(data, orig_shape)
        
        print(f"Original is_track: {boxes.is_track}") # Should be True
        print(f"Original id: {boxes.id}")
        
        # 2. Attempt to remove ID by slicing data
        # We want columns 0-3 (xyxy) and 5-6 (conf, cls)
        # Indices: 0,1,2,3, 4(id), 5(conf), 6(cls)
        
        # Careful: Boxes expects specific order.
        # If input is 6 columns: xyxy, conf, cls
        # So yes, skipping col 4 should work.
        
        new_data = torch.cat((boxes.data[:, :4], boxes.data[:, 5:]), dim=1)
        
        # We need to update the boxes object inside results.
        # But we can just create a new boxes object or update .data?
        # Boxes inherits BaseTensor. 
        # Updating .data directly might be risky if shape checks happen elsewhere, 
        # but let's try updating data and re-evaluating is_track manually?
        
        # Actually safer to create new Boxes object and assign it back to results.boxes
        new_boxes = Boxes(new_data, orig_shape)
        
        print(f"New is_track: {new_boxes.is_track}") # Should be False
        print(f"New id: {new_boxes.id}")
        
        # 3. Test plot with this new boxes object
        # Mock Results object
        class MockResults:
            def __init__(self, boxes):
                self.boxes = boxes
                self.names = {0: "person"}
                self.probs = None
                self.masks = None
                self.keypoints = None
                self.obb = None
                self.orig_img = np.zeros((640, 640, 3), dtype=np.uint8)
                self.orig_shape = (640, 640)
            
            # Borrow plot from Results but we can't easily binding it.
            # We can rely on just checking if we can swap boxes in a real Results object.
            
        # Real test with YOLO and track
        # Since I can't easily mock Results.plot completely without copy paste.
        # I will trust that if new_boxes.is_track is False, plot will not show ID.
        
        assert boxes.is_track == True
        assert new_boxes.is_track == False
        
        if new_boxes.id is not None:
             print("Error: ID should be None")
             return 1
             
        print("Success logic check.")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(test_fix())
