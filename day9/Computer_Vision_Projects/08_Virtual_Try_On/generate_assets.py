
import cv2
import numpy as np
import os

def create_shirt_asset(filename, color):
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
    
    # Draw Shirt with Alpha 255
    # Color is BGR
    b, g, r = color
    cv2.fillPoly(img, [pts], (b, g, r, 255))
    
    # Add simple shading/texture
    # Neckline
    cv2.ellipse(img, (200, 50), (100, 50), 0, 0, 180, (b-20, g-20, r-20, 255), 2)
    # Fold
    cv2.line(img, (100, 150), (200, 200), (b-30, g-30, r-30, 255), 2)
    
    cv2.putText(img, "FASHION", (140, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255, 200), 2)
    
    os.makedirs("Resources", exist_ok=True)
    cv2.imwrite(f"Resources/{filename}", img)
    print(f"Created {filename}")

if __name__ == "__main__":
    colors = [
        (0, 0, 255),   # Red
        (255, 0, 0),   # Blue
        (0, 255, 0),   # Green
        (0, 255, 255), # Yellow
        (255, 0, 255)  # Purple
    ]
    
    for i, color in enumerate(colors):
        create_shirt_asset(f"shirt_{i}.png", color)
