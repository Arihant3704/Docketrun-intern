import torch
import torch_pruning as tp
from ultralytics import YOLO
import os
import copy

def prune_model(model_path, output_path, pruning_ratio=0.2):
    print(f"Loading model: {model_path}")
    # Load Ultralytics model
    yolo_model = YOLO(model_path)
    # Fuse and set to eval
    print("Fusing model...")
    yolo_model.fuse()
    model = yolo_model.model
    model.eval()
    
    # Input for dependency graph tracing
    example_inputs = torch.randn(1, 3, 640, 640)
    
    try:
        print("Attempting structured pruning with torch_pruning...")
        # 1. Importance criterion
        imp = tp.importance.MagnitudeImportance(p=1) 

        ignored_layers = []
        # Aggressively ignore the head layers (usually indices > 15 in YOLOv8n-seg)
        # The structure is model.model (nn.Sequential). 
        # We can ignore everything after the backbone (approx layer 10) to be safe, 
        # or just the complex head.
        
        # Let's inspect the last module
        if isinstance(model.model, torch.nn.Sequential):
            head_idx = len(model.model) - 1
            print(f"Identifying potential head at index {head_idx}")
            ignored_layers.append(model.model[head_idx])
            
            # Also ignore the split/concat heavy PANet layers if needed
            # For now, let's just ignore the last module (Segment/Detect)
            
        pruner = tp.pruner.MagnitudePruner(
            model,
            example_inputs,
            importance=imp,
            iterative_steps=1,
            pruning_ratio=pruning_ratio,
            ignored_layers=ignored_layers, 
        )

        print(f"Pruning model with ratio {pruning_ratio}...")
        base_macs, base_nparams = tp.utils.count_ops_and_params(model, example_inputs)
        print(f"Base MACs: {base_macs/1e9:.2f} G, Params: {base_nparams/1e6:.2f} M")

        pruner.step()

        # Check output
        pruned_macs, pruned_nparams = tp.utils.count_ops_and_params(model, example_inputs)
        print(f"Pruned MACs: {pruned_macs/1e9:.2f} G, Params: {pruned_nparams/1e6:.2f} M")
        print(f"Reduction: MACs -{(1-pruned_macs/base_macs)*100:.1f}%, Params -{(1-pruned_nparams/base_nparams)*100:.1f}%")
        
    except Exception as e:
        print(f"\nStructured pruning failed: {e}")
        print("Falling back to Unstructured Pruning (Zeroing small weights)...")
        # Global unstructured pruning
        import torch.nn.utils.prune as prune
        
        parameters_to_prune = []
        for name, m in model.named_modules():
            if isinstance(m, torch.nn.Conv2d):
                parameters_to_prune.append((m, 'weight'))
                
        print(f"Pruning {len(parameters_to_prune)} Conv2d layers unstructured...")
        prune.global_unstructured(
            parameters_to_prune,
            pruning_method=prune.L1Unstructured,
            amount=pruning_ratio,
        )
        
        # Make pruning permanent
        for m, name in parameters_to_prune:
            prune.remove(m, name)
            
        print("Unstructured pruning complete.")

    # Save
    # We need to save it as a YOLO compatible pt file.
    # Ultralytics objects wrap the model, so we update the inner model and save using torch.save
    # or use yolo_model.save() if it respects the changes.
    
    # Update the yolo_model.model with the pruned pth module
    yolo_model.model = model
    
    # Use torch.save explicitly to preserve Ultralytics format structure (ckpt)
    # Re-wrap in the dictionary structure Ultralytics expects
    ckpt = {
        'model': yolo_model.model,
        'train_args': {}, # Minimal args
        'epoch': -1,
    }
    torch.save(ckpt, output_path)
    print(f"Pruned model saved to {output_path}")

def main():
    model_name = "yoloe-26n-seg.pt"
    model_path = os.path.join(os.path.dirname(__file__), model_name)
    output_path = os.path.join(os.path.dirname(__file__), "yoloe-26n-seg_pruned.pt")
    
    if os.path.exists(model_path):
        prune_model(model_path, output_path, pruning_ratio=0.20)
    else:
        print(f"Model {model_path} not found.")

if __name__ == "__main__":
    main()
