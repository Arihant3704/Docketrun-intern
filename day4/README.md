# YOLO Commands

This file documents the commands used to process the video `Safety_Harness_the_Right_Way_480P.mp4` with the YOLO model `yolo26colourdataset.pt`.

## Commands

### 1. Without Tracker

```bash
python run_yolo.py yolo26colourdataset.pt Safety_Harness_the_Right_Way_480P.mp4 no_tracker_output.mp4
```

### 2. With Tracker

```bash
python run_yolo.py yolo26colourdataset.pt Safety_Harness_the_Right_Way_480P.mp4 with_tracker_output.mp4 botsort.yaml
```

### 3. With Lower Confidence Threshold (25%)

```bash
python run_yolo.py yolo26colourdataset.pt Safety_Harness_the_Right_Way_480P.mp4 conf_25_output.mp4 None 0.25
```