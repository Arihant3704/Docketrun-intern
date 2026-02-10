from torchvision import models
import torch
import numpy as np
import cv2
import sys
import os
import torchvision.transforms as T
from PIL import Image

def segment_image(image_path, output_path='output.jpg'):
    fcn = models.segmentation.fcn_resnet50(pretrained=True).eval()

    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    img = Image.open(image_path)
    trf = T.Compose([T.Resize(256),
                     T.CenterCrop(224),
                     T.ToTensor(),
                     T.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])])
    inp = trf(img).unsqueeze(0)
    
    # Run model
    out = fcn(inp)['out']
    om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
    
    # Define colors for different classes (simplified)
    def decode_segmap(image, nc=21):
        label_colors = np.array([(0, 0, 0),  # 0=background
                       # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                       (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                       (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                       # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                       (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                       # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                       (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

        r = np.zeros_like(image).astype(np.uint8)
        g = np.zeros_like(image).astype(np.uint8)
        b = np.zeros_like(image).astype(np.uint8)
        
        for l in range(0, nc):
            idx = image == l
            r[idx] = label_colors[l, 0]
            g[idx] = label_colors[l, 1]
            b[idx] = label_colors[l, 2]
            
        rgb = np.stack([r, g, b], axis=2)
        return rgb

    rgb = decode_segmap(om)
    
    # Resize back to original or save as is (here saving the processed crop)
    cv2.imwrite(output_path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    print(f"Segmentation completed. Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        segment_image(sys.argv[1])
    else:
        if os.path.exists("input.jpg"):
            segment_image("input.jpg")
        else:
            print("Usage: python main.py <image_path>")
