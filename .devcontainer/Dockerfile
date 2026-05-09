FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# =========================
# system deps (ROS + OpenCV ABI)
# =========================
RUN apt-get update && apt-get install -y \
    git curl vim build-essential \
    python3-pip python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Python core (LOCKED)
# =========================
RUN pip3 install --no-cache-dir \
    numpy==1.26.4 \
    transforms3d

# =========================
# PyTorch GPU (STABLE cu118)
# =========================
RUN pip3 install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu118

# =========================
# YOLO
# =========================
RUN pip3 install --no-cache-dir ultralytics

# =========================
# ROS env
# =========================
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

WORKDIR /ros2_ws