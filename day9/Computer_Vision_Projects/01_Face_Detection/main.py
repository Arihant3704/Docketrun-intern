import cv2
import sys
import os

def detect_faces(image_path=None, output_path='output.jpg'):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if image_path:
        # Read the input image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return
    else:
        # functionality for webcam (not used in this resume build step)
        print("No image path provided. Usage: python main.py <image_path>")
        return

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Save the output
    cv2.imwrite(output_path, img)
    print(f"Found {len(faces)} faces. Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        detect_faces(sys.argv[1])
    else:
        # Default to input.jpg if exists
        if os.path.exists("input.jpg"):
            detect_faces("input.jpg")
        else:
            print("Please provide an image path.")
