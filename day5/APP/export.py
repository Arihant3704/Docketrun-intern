from ultralytics import YOLO

# Load the ONNX segmentation model
model = YOLO("yoloe-26n-seg.onnx", task="segment")

# Run inference on an image
results = model.predict(source="download.jpeg", conf=0.25)

# Visualize results
for result in results:
    result.show()  # Display to screen
    result.save(filename="result.jpg")  # Save to disk

