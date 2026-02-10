import cv2
import pytesseract
import sys
import os

def ocr_scanner(image_path, output_path='output.jpg', text_output='output.txt'):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Perform OCR
    text = pytesseract.image_to_string(gray)
    
    # Save text output
    with open(text_output, "w") as f:
        f.write(text)
    
    # Annotate image
    h, w, _ = image.shape
    boxes = pytesseract.image_to_boxes(gray)
    for b in boxes.splitlines():
        b = b.split(' ')
        image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imwrite(output_path, image)
    print(f"OCR completed.\nText saved to {text_output}\nAnnotated image saved to {output_path}")
    print("Extracted TextPreview:\n" + text[:100] + "...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ocr_scanner(sys.argv[1])
    else:
        if os.path.exists("input.jpg"):
            ocr_scanner("input.jpg")
        else:
            print("Usage: python main.py <image_path>")
