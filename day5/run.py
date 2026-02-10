from ultralytics import YOLO

# Initialize model
model = YOLO("yoloe-26n-seg.pt")  # or select yoloe-26s/m-seg.pt for different sizes

# Set text prompt to detect person and bus. You only need to do this once after you load the model.
names = ["Harness on person","Fall Protection"]
model.set_classes(names, model.get_text_pe(names))

# Run detection on the given image
results = model.predict("1.jpg")




results = model.predict("download.jpeg")


# Show results
results[0].show()
