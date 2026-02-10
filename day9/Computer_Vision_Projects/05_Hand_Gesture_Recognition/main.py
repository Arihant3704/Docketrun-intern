import cv2
import mediapipe as mp
import sys
import os

def recognize_gestures(image_path, output_path='output.jpg'):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    
    # Initialize MediaPipe Hands
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return
            
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_hand_landmarks:
            print("No hands found.")
            return

        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
        cv2.imwrite(output_path, annotated_image)
        print(f"Hand landmarks drawn. Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        recognize_gestures(sys.argv[1])
    else:
        if os.path.exists("input.jpg"):
            recognize_gestures("input.jpg")
        else:
            print("Usage: python main.py <image_path>")
