
import cv2
import numpy as np
import os

def create_shirt_asset():
    # Create a 400x400 BGRA image (transparent)
    img = np.zeros((400, 400, 4), dtype=np.uint8)
    
    # Define T-Shirt Points (Simple Polygon)
    pts = np.array([
        [100, 50],  # Left Neck
        [300, 50],  # Right Neck
        [350, 100], # Right Shoulder
        [350, 150], # Right Sleeve Bottom
        [300, 150], # Right Armpit
        [300, 350], # Right Bottom
        [100, 350], # Left Bottom
        [100, 150], # Left Armpit
        [50, 150],  # Left Sleeve Bottom
        [50, 100]   # Left Shoulder
    ], np.int32)
    
    pts = pts.reshape((-1, 1, 2))
    
    # Draw Red Shirt
    # Color: BGR = (0, 0, 255), Alpha = 255
    cv2.fillPoly(img, [pts], (0, 0, 255, 255))
    
    # Add some "texture" or text
    cv2.putText(img, "AI STYLE", (130, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 2)
    
    os.makedirs("Resources", exist_ok=True)
    cv2.imwrite("Resources/shirt_asset.png", img)
    print("Created synthetic shirt_asset.png")

if __name__ == "__main__":
    create_shirt_asset()
