# Dockerized YOLO Live Application

This directory contains a Dockerized version of the YOLO live inference application.

## Prerequisites

- Docker installed on your system.
- One of the following for GUI display:
    - **Linux**: X11 server (standard on most distros).
    - **Windows**: WSL2 with VcXsrv or similar X server.
    - **macOS**: XQuartz.

## Setup

1.  **Navigate to the directory**:
    ```bash
    cd day6
    ```

2.  **Build the Docker image**:
    ```bash
    docker build -t yolo-live .
    ```

## Running the Application

### Quick Start (Linux)

You can use the provided shell script to build (if needed) and run the application:

```bash
chmod +x run.sh
./run.sh
```

### Manual Run

To run the application manually with access to your webcam and display, use the following command.

#### Linux

You need to pass the X11 socket and the display environment variable, and map the video device.

```bash
docker run --rm -it \
    --device=/dev/video0:/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    yolo-live
```

**Note**: If you encounter `xhost` permission errors, run `xhost +local:docker` on your host machine before running the container.

#### Windows (WSL2)

If using VcXsrv, ensure it is running with "Disable access control" checked.

```bash
docker run --rm -it \
    --device=/dev/video0:/dev/video0 \
    -e DISPLAY=host.docker.internal:0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    yolo-live
```

#### macOS

Ensure XQuartz is running and "Allow connections from network clients" is enabled.

```bash
xhost + 127.0.0.1
docker run --rm -it \
    -e DISPLAY=host.docker.internal:0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device=/dev/video0:/dev/video0 \
    yolo-live
```

## Files

- `app.py`: The main Python application (originally `live.py`).
- `yolo26colourdataset.pt`: The YOLO detection model.
- `Dockerfile`: Configuration for building the Docker image.
- `run.sh`: Helper script to run the container on Linux.
