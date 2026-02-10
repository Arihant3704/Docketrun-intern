# Day 5: Model Optimization, Conversion & Deployment

This directory contains the work for **Day 5**, focusing on optimizing YOLOv8 models for efficient deployment. The primary goals were to convert PyTorch models to ONNX format, apply Half Precision (FP16) quantization, and benchmark the trade-offs between model size and inference speed.

## 📂 Files

- **`convert.py`**: A utility script to convert YOLO `.pt` models to ONNX and ONNX FP16 formats.
- **`benchmark.py`**: A benchmarking script that measures File Size, Average Inference Time, FPS, and Confidence scores across different model formats.
- **`benchmark_report.md`**: The generated report from the benchmark run.
- **`run.py`**: Simple inference script for testing model predictions.

## 🚀 Usage

### 1. Convert Models
To convert existing `.pt` models to ONNX and FP16:
```bash
python convert.py
```
This will generate `.onnx` (FP32) and `_half.onnx` (FP16) files for each model.

### 2. Run Benchmark
To compare performance across all available models:
```bash
python benchmark.py
```
This generates `benchmark_report.md` with a summary table.

## 📊 Results Summary

We compared the original PyTorch models against their ONNX and ONNX FP16 counterparts.

**Key Findings:**
- **Size Reduction**: FP16 quantization reduced the model size by **~10%** for detection models and **~46%** for segmentation models.
- **Performance**: 
  - ONNX FP16 is optimized for GPU execution. On CPU, it may encounter compatibility issues or slower performance due to lack of native half-precision support.
  - For CPU deployment, standard ONNX (FP32) or PyTorch (OpenVINO) is often preferred.
  - For GPU deployment, ONNX FP16 typically offers a **2x-3x speedup**.

### Benchmark Data (CPU)

| Model | Size (MB) | Avg Time (ms) | FPS |
|-------|-----------|---------------|-----|
| `yolo26colourdataset.pt` | 6.23 | ~106 | ~9.4 |
| `yoloe-26n-seg.pt` | 10.93 | ~177 | ~5.6 |
