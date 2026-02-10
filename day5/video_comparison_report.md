# Video Inference Comparison Report

**Input Video**: `Construction_Safety_Hazard_CCTV_Video.mp4`

| Model | Status | Avg FPS | Total Time (s) | Output |
|-------|--------|---------|----------------|--------|
| yolo26colourdataset.pt | Success | 35.73 | 5.37 | [Link](output_yolo26colourdataset.pt_Construction_Safety_Hazard_CCTV_Video.mp4) |
| yolo26colourdataset.onnx | Success | 5.27 | 36.40 | [Link](output_yolo26colourdataset.onnx_Construction_Safety_Hazard_CCTV_Video.mp4) |
| yolo26colourdataset_half.onnx | Failed: [ONNXRuntimeError] : 10 : INVALID_GRAPH... | 0.00 | 0.00 | N/A |
| yoloe-26n-seg.pt | Success | 43.84 | 4.38 | [Link](output_yoloe-26n-seg.pt_Construction_Safety_Hazard_CCTV_Video.mp4) |
| yoloe-26n-seg.onnx | Success | 4.52 | 42.47 | [Link](output_yoloe-26n-seg.onnx_Construction_Safety_Hazard_CCTV_Video.mp4) |
| yoloe-26n-seg_half.onnx | Failed: [ONNXRuntimeError] : 10 : INVALID_GRAPH... | 0.00 | 0.00 | N/A |
