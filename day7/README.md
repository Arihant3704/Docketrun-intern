# Day 7: Conveyor Belt Analysis with YOLO + Optical Flow + Canny Edge

## Overview
This project performs real-time analysis of conveyor belt footage to detect:
1.  **Belt Movement**: Using dense optical flow (Farneback method) on the detected belt region.
2.  **Object/Coal Presence**: Using Canny Edge Detection to identify textured objects on the belt.

## Models
-   **Belt Detection**: Local YOLO model (`best.pt`) trained to detect 'Belt'.
-   **Coal Detection**: Traditional Computer Vision (Canny Edge) is used instead of a second ML model for speed and robustness on texture.

## Key Files
-   `analyze_day7.py`: Main analysis script.
-   `best.pt`: YOLO weights for belt detection.
-   `a.mp4`: Input video.
-   `output_a.mp4`: Annotated output video.

## Usage
Run the analysis script:
```bash
python3 analyze_day7.py
```

## Configuration
-   **`EDGE_THRESHOLD`**: Tuned to **5075** to distinguish between the empty belt and coal.
-   **`movement_threshold`**: Optical flow magnitude threshold for movement detection.
