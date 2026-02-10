
import cv2
import numpy as np

def create_variants():
    # Load the first real shirt
    img = cv2.imread("Resources/shirt_0.png", cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: shirt_0.png not found")
        return

    # Convert to HSV (ignoring alpha for now)
    bgr = img[:, :, :3]
    alpha = img[:, :, 3]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
    # Variant 1: Shift Hue by 60 (Yellow/Green)
    hsv_v1 = hsv.copy()
    hsv_v1[:, :, 0] = (hsv_v1[:, :, 0] + 60) % 180
    bgr_v1 = cv2.cvtColor(hsv_v1, cv2.COLOR_HSV2BGR)
    
    img_v1 = np.dstack((bgr_v1, alpha))
    cv2.imwrite("Resources/shirt_3.png", img_v1)
    print("Created shirt_3.png (Hue Shift 1)")
    
    # Variant 2: Shift Hue by 120 (Blue/Purple)
    hsv_v2 = hsv.copy()
    hsv_v2[:, :, 0] = (hsv_v2[:, :, 0] + 120) % 180
    bgr_v2 = cv2.cvtColor(hsv_v2, cv2.COLOR_HSV2BGR)
    
    img_v2 = np.dstack((bgr_v2, alpha))
    cv2.imwrite("Resources/shirt_4.png", img_v2)
    print("Created shirt_4.png (Hue Shift 2)")

if __name__ == "__main__":
    create_variants()
