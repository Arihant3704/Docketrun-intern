import math
import cv2
from ultralytics import YOLO

class PoseDetector:
    def __init__(self, model_path='yolov8n-pose.pt', device=None):
        """
        Initialize the PoseDetector with a YOLOv8-pose model.
        """
        self.model = YOLO(model_path)
        self.device = device
        self.results = None

    def find_pose(self, img, draw=True):
        """
        Finds the pose landmarks in an image using YOLOv8.
        """
        self.results = self.model(img, verbose=False, device=self.device)[0]  # Run inference
        
        if draw:
            # Visualize the results on the frame
            img = self.results.plot()
        
        return img

    def get_position(self, img, draw=True):
        """
        Extracts landmark positions from the results.
        Returns a list of landmarks [id, x, y, confidence].
        """
        lm_list = []
        if self.results and self.results.keypoints is not None:
             # Extract keypoints (x, y, confidence)
            keypoints = self.results.keypoints.data[0].cpu().numpy() 
            
            for id, lm in enumerate(keypoints):
                h, w, c = img.shape
                # YOLO output is normalized? No, usually absolute coordinates
                cx, cy, conf = int(lm[0]), int(lm[1]), lm[2]
                lm_list.append([id, cx, cy, conf])
                
                if draw:
                     cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        
        return lm_list

    def find_angle(self, img, p1, p2, p3, lm_list, draw=True):
        """
        Calculate the angle between three points (p1-p2-p3).
        p1, p2, p3 are indices of landmarks in lm_list.
        """
        if len(lm_list) < max(p1, p2, p3) + 1:
            return 0

        # Get the coordinates
        x1, y1 = lm_list[p1][1], lm_list[p1][2]
        x2, y2 = lm_list[p2][1], lm_list[p2][2]
        x3, y3 = lm_list[p3][1], lm_list[p3][2]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        return angle
