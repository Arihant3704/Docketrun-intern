# Day 11: Advanced Pose Detection & Gym Trainer

This project implements a real-time pose detection application using YOLOv8-pose. It features a "Gym Trainer" mode that counts repetitions for exercises like squats and pushups, providing visual feedback on form.

## Features

- **Real-time Pose Estimation**: Uses YOLOv8n-pose for fast and accurate keypoint detection.
- **Exercise Rep Counter**: Automatically counts reps for Squats and Pushups based on joint angles.
- **Form Analysis**: Visual feedback for "Good" and "Bad" form (e.g., deep enough squat).
- **FPS Display**: Real-time performance monitoring.

## Installation

1.  **Clone/Navigate to directory**:
    ```bash
    cd /home/arihant/intern/day11
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main application:

```bash
# Use Webcam (Default)
python main.py

# Use a video file
python main.py --source path/to/video.mp4

# Select Exercise Mode (Default: squat)
python main.py --exercise pushup
```

## Controls

- `q`: Quit application

## Custom Mode

The `custom` exercise mode counts a repetition when the angle:
1.  Starts at or below **200 degrees**.
2.  Goes above **290 degrees**.
