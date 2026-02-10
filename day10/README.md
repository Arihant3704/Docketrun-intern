# Video Labeler Pro

A professional-grade, single-window video labeling application powered by **SAM 2.1** and **Tkinter**.

## Features
- **Unified Interface**: Single window with Toolbox, Timeline, and Zoomable Canvas.
- **Backend Modules**:
  - **Threaded Inference**: UI never freezes during propagation.
  - **Chunked Processing**: Efficiently handles long videos.
- **Data Management**:
  - **Project System**: Auto-saves logic and crash recovery.
  - **Undo/Redo**: Full history stack for annotations.
  - **Validator**: Ensures dataset integrity before export.
  - **YOLO Export**: Direct export to standard YOLO segmentation format.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -e .
   ```

2. **Run Application**
   ```bash
   video-labeler
   # OR
   python labeler_app/main.py
   ```

## Workflow
1. **Detect Mode**: Click objects to segment them using SAM 2.
2. **Track Mode**: Use the "Track" button (or Spacebar) to propagate masks.
3. **Edit Mode**: Select objects from the list to rename or delete.
4. **Export**: Click "Export YOLO" to generate datasets in `projects/<name>/export_yolo`.

## Architecture
- `core/`: State management (`AnnotationManager`), persistence (`ProjectManager`), and logic.
- `backend/`: Interfaces for SAM 2 (`SAM2Provider`) and Exporters.
- `ui/`: Tkinter components (`MainWindow`, `ZoomCanvas`, etc.).
- `controller.py`: Central mediator handling business logic.

## Configuration
Update `controller.py` to point to your specific SAM 2 checkpoint:
```python
chkpt = "sam2_repo/checkpoints/sam2.1_hiera_base_plus.pt"
cfg = "configs/sam2.1/sam2.1_hiera_b+.yaml"
```
