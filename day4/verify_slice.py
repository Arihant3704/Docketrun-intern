import torch
from ultralytics.engine.results import Boxes

def test_slice_replace():
    # Setup data with track_id (7 cols)
    data = torch.tensor([[100, 100, 200, 200, 1.0, 0.9, 0.0]])
    orig_shape = (640, 640)
    boxes = Boxes(data, orig_shape)
    
    # Iterate - check it has id
    for d in boxes:
        if not d.is_track:
            print("Fail: Item should have is_track=True")
            return 1
            
    # Modify
    new_data = torch.cat((boxes.data[:, :4], boxes.data[:, 5:]), dim=1)
    new_boxes = boxes.__class__(new_data, boxes.orig_shape)
    
    # Check new boxes
    if new_boxes.is_track:
        print("Fail: New boxes should have is_track=False")
        return 1
        
    # Iterate new boxes
    for d in new_boxes:
        if d.is_track:
            print("Fail: New item should have is_track=False")
            return 1
        if d.id is not None:
            print("Fail: New item id should be None")
            return 1
            
    print("Success: Slicing works!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(test_slice_replace())
