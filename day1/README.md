# Automated Dataset Annotation and Evaluation

This project provides a comprehensive workflow for automated dataset annotation and evaluation using state-of-the-art models: **Grounding DINO** for zero-shot object detection and **SAM (Segment Anything Model)** for high-quality segmentation.

## Features

- **Zero-Shot Object Detection**: Detect arbitrary objects using textual prompts with Grounding DINO.
- **Automated Annotation**: Use Grounding DINO and SAM together to automatically generate bounding box and mask annotations for your datasets.
- **Dataset Evaluation**: Compare automated annotations with manual "gold standard" annotations to calculate metrics like mAP and confusion matrices.
- **Inference Tutorials**: Step-by-step Jupyter notebooks for single image and dataset-level processing.

## Project Structure

- `automated-dataset-annotation-and-evaluation-with-grounding-dino.ipynb`: Tutorial on zero-shot detection and dataset evaluation using Grounding DINO.
- `automated-dataset-annotation-and-evaluation-with-grounding-dino-and-sam.ipynb`: Advanced tutorial combining Grounding DINO and SAM for full mask annotation.
- `AI Development Lifecycle Explained.docx`: Background documentation on the developer Roadmap and lifecycle.
- `1.html`: Related web content/documentation.

## Getting Started

### Prerequisites

- Python 3.x
- GPU Acceleration (highly recommended for inference)
- Key Libraries: `torch`, `supervision`, `roboflow`, `groundingdino`, `segment_anything`

### Installation

1. Clone the Grounding DINO repository:
   ```bash
   git clone https://github.com/IDEA-Research/GroundingDINO.git
   cd GroundingDINO
   git checkout feature/more_compact_inference_api
   pip install -q -e .
   ```

2. Install additional dependencies:
   ```bash
   pip install -q roboflow dataclasses-json onemetric supervision
   ```

3. Download model weights (refer to the notebooks for specific URLs).

## Usage

Open the provided Jupyter notebooks and follow the step-by-step instructions:

1. **Configure Environment**: Set up GPU and install dependencies.
2. **Load Models**: Load Grounding DINO and SAM weights.
3. **Run Inference**: Use text prompts to detect objects in images or entire datasets.
4. **Evaluate/Annotate**: Generate annotations in COCO format or evaluate performance against existing labels.

## References

- [Grounding DINO GitHub](https://github.com/IDEA-Research/GroundingDINO)
- [Segment Anything Model (SAM) GitHub](https://github.com/facebookresearch/segment-anything)
- [Roboflow Notebooks](https://github.com/roboflow/notebooks)
