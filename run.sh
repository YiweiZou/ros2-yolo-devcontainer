#!/bin/bash

docker run -it \
  --name ros2_yolo_dev \
  --gpus all \
  --network host \
  -v ~/ros2_ws:/ros2_ws \
  -v ~/.ssh:/root/.ssh \
  ros2-yolo-final \
  bash