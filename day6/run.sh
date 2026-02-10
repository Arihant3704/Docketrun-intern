#!/bin/bash

# Allow docker to access the X server
xhost +local:docker

# Run the container
docker run --rm -it \
    --device=/dev/video0:/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    yolo-live
