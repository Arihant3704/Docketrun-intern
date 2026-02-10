import cv2
import numpy as np

class GymTrainer:
    def __init__(self, exercise_type='squat'):
        self.exercise_type = exercise_type
        self.count = 0
        self.dir = 0  # 0 for going down, 1 for going up
        self.feedback = "Fix Form"
        
        # Defining landmarks for exercises (Left side defaults)
        # COCO Keypoints: 
        # 5: L-Shoulder, 7: L-Elbow, 9: L-Wrist
        # 11: L-Hip, 13: L-Knee, 15: L-Ankle
        if self.exercise_type == 'squat':
            self.p1, self.p2, self.p3 = 11, 13, 15
        elif self.exercise_type == 'pushup':
            self.p1, self.p2, self.p3 = 5, 7, 9
        elif self.exercise_type == 'custom':
            # Default to squat points for custom, or could be user defined
            self.p1, self.p2, self.p3 = 11, 13, 15
        else:
            # Default to squat
            self.p1, self.p2, self.p3 = 11, 13, 15

    def processing(self, img, angle):
        """
        Process the angle to count reps and provide feedback.
        """
        percentage = 0
        bar = 0
        
        # Squat Logic
        if self.exercise_type == 'squat':
            # Angle range for squat: 170 (standing) -> 70 (deep squat)
            # Normalize angle to percentage (0% standing, 100% deep)
            percentage = np.interp(angle, (70, 160), (100, 0))
            bar = np.interp(angle, (70, 160), (100, 650)) # Bar height on screen
            
            # Check states
            color = (255, 0, 255)
            if percentage == 100:
                color = (0, 255, 0)
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if percentage == 0:
                color = (0, 255, 0)
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0
                    
            # Feedback based on depth
            if percentage > 90:
                self.feedback = "Great Depth!"
            elif percentage < 20:
                self.feedback = "Go Lower"
            else:
                self.feedback = "Good"

        # Pushup Logic
        elif self.exercise_type == 'pushup':
             # Angle range: 170 (up) -> 80 (down)
            percentage = np.interp(angle, (80, 160), (100, 0))
            bar = np.interp(angle, (80, 160), (100, 650))
            
            color = (255, 0, 255)
            if percentage == 100:
                color = (0, 255, 0)
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if percentage == 0:
                color = (0, 255, 0)
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0
                    
        # Custom Logic (Angle 200 -> 290)
        elif self.exercise_type == 'custom':
             # Logic: Count if angle starts <= 200 and goes >= 290
             
             color = (255, 0, 255)
             
             # State 0: Waiting to go below 200 (Reset)
             if angle <= 200:
                 color = (0, 255, 0)
                 if self.dir == 0:
                     self.dir = 1
                     self.feedback = "Go Up to 290"
             
             # State 1: Waiting to go above 290 (Count)
             if angle >= 290:
                 color = (0, 255, 0)
                 if self.dir == 1:
                     self.count += 0.5 # Using 0.5 if we want full cycle, but user said "consider as one re"
                     # Usually my logic is 0.5 for down, 0.5 for up.
                     # Let's stick to the pattern: 
                     # If we want 1 rep on reaching 290:
                     # But we need to reset. 
                     # Let's do: 0.5 on reset (200), 0.5 on complete (290).
                     self.count += 0.5
                     self.dir = 0
                     self.feedback = "Go Down to 200"
             
             # Visualization: Map 200-290 range
             percentage = np.interp(angle, (200, 290), (0, 100))
             bar = np.interp(angle, (200, 290), (650, 100))
        
        # Draw Bar
        if bar > 0:
             cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
             cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
             cv2.putText(img, f'{int(percentage)}%', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)

        # Draw Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(self.count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

        return img, int(self.count)
