import os
import torch
from ultralytics import YOLO
import onnx
# from onnxconverter_common import float16 # Dropping this for now as it causes issues

def convert_to_onnx(model_path, output_path, simplify=True, half=False):
    print(f"Converting {model_path} to ONNX (half={half})...")
    model = YOLO(model_path)
    # Export the model
    try:
        path = model.export(format="onnx", dynamic=True, simplify=simplify, half=half)
    except Exception as e:
        print(f"Export failed with half={half}: {e}")
        return None
        
    # Move/Rename if necessary
    if path and path != output_path:
        os.rename(path, output_path)
    print(f"Saved ONNX model to {output_path}")
    return output_path

def main():
    models = [
        "yolo26colourdataset.pt",
        "yoloe-26n-seg.pt"
    ]
    
    for model_name in models:
        base_name = os.path.splitext(model_name)[0]
        model_path = os.path.join(os.path.dirname(__file__), model_name)
        
        if not os.path.exists(model_path):
            print(f"Model {model_path} not found, skipping.")
            continue
            
        # 1. Convert to ONNX FP16 (Native Export)
        onnx_half_path = os.path.join(os.path.dirname(__file__), f"{base_name}_half.onnx")
        try:
            convert_to_onnx(model_path, onnx_half_path, half=True)
        except Exception:
            print("Native half export failed.")

        # 2. Convert to ONNX (FP32)
        onnx_path = os.path.join(os.path.dirname(__file__), f"{base_name}.onnx")
        convert_to_onnx(model_path, onnx_path, half=False)

if __name__ == "__main__":
    main()
