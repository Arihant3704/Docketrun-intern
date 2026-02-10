# Video Labeling Tool - User Manual

This tool provides an efficient interface for labeling objects in videos using the SAM 2 (Segment Anything Model 2) architecture. It supports interactive segmentation, automated tracking, and YOLO format export.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- CUDA-enabled GPU (Recommended)
- `torch`, `torchvision`, `opencv-python`, `Pillow`, `numpy`
- `sam2` (included in `sam2_repo`)

### Installation
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Running the Tool
Execute the main script from the `day10` directory:
```bash
python3 run_labeler.py
```

---

## 🛠️ Usage Workflow

### 1. Project Management
- **Create New Project**:
    - Click **"New Project"**.
    - Enter a **Project Name**.
    - Select a **Video File** (`.mp4`, `.avi`, etc.).
    - Enter **Object Classes** (comma-separated, e.g., `helmet,vest,person`).
- **Open Existing Project**:
    - Click **"Open Project"**.
    - Select a previously created project directory (e.g., `projects/MyProject`).

### 2. Interface Overview
- **Canvas (Center)**: Displays the video frame.
    - **Zoom**: Scroll Mouse Wheel (or 2-finger scroll).
    - **Pan**: Click and Drag with Left Mouse Button (outside of objects) or Middle Mouse Button.
    - **Right-Click**: Opens context menu for objects (Rename/Delete).
- **Timeline (Bottom)**:
    - **Slider**: Scrub through video frames.
    - **Play/Pause**: Toggle video playback.
    - **Step < / >**: Move one frame backward/forward.
- **Toolbox (Left)**:
    - **Modes**:
        - **Detect (SAM)**: Active labeling mode. Click to segment.
        - **Track**: View mode (prevents accidental edits).
        - **Edit**: Manual refinement (if implemented).
    - **Objects List**: Manage active objects.
        - **Add**: Create a new object ID.
        - **Rename**: Change class name of selected object.
        - **Del**: Delete selected object and its masks.
    - **Propagate**: Run tracker to propagate masks to future frames.
    - **Export YOLO**: Save annotations to disk.

### 3. Labeling & Tracking
1.  **Add an Object**:
    - Ensure **Detect (SAM)** mode is selected.
    - Select an object ID from the list (or click **Add** to create a new one).
    - **Left Click** on the object in the image to add a **Positive Point** (Green).
    - **Right Click** on background/errors to add a **Negative Point** (Red).
    - The mask will update in real-time.

2.  **Propagate (Track)**:
    - Once the mask is good on the current frame, click **Propagate...**.
    - Enter the number of frames to track (e.g., `30` or `0` for all subsequent frames).
    - The tool will automatically segment the object in future frames.

3.  **Refinement**:
    - Scrub through the propagated frames.
    - If tracking drifts, stop at the bad frame.
    - Add new points to correct the mask.
    - Click **Propagate...** again to update future frames with the correction.

### 4. Exporting Data
- Click **Export YOLO**.
- Annotations are saved in the `export_yolo` folder within your project directory.
- Format: standard YOLO `.txt` files (one per frame) containining `class_id x_center y_center width height`.

---

## ⌨️ Shortcuts & Controls
- **Left Click**: Add Positive Point (in Detect Mode).
- **Right Click**: Add Negative Point (in Detect Mode) / Context Menu.
- **Mouse Wheel**: Zoom In/Out.
- **Spacebar**: Toggle Play/Pause.
- **Left/Right Arrow**: Previous/Next Frame.

## 📂 Project Structure
Projects are saved in the `projects/` directory.
```
projects/
  └── MyProject/
      ├── manifest.json       # Project metadata
      ├── annotations.json    # Object and mask data
      └── export_yolo/        # Exported labels
```
