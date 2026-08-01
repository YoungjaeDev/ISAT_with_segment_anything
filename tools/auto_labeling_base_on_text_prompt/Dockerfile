FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      libgl1-mesa-glx \
      libglib2.0-0 \
      libsm6 \
      libxext6 \
      libxrender-dev \
      libgomp1 \
      && rm -rf /var/lib/apt/lists/*

# 中文显示支持
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    fonts-wqy-microhei \
    && locale-gen zh_CN.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8

#RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
#    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir \
    "torch>=2.3.0" \
    torchvision \
    opencv-python-headless \
    pycocotools \
    "timm>=1.0.17" \
    "numpy>=1.26,<2" \
    tqdm \
    "ftfy==6.1.1" \
    scikit-image \
    pillow \
    pyyaml \
    shapely \
    "hydra-core>=1.3.2" \
    "tqdm>=4.66.1" \
    fuzzywuzzy \
    "iopath>=0.1.10" \
    orjson \
    requests \
    einops \
    psutil \
    regex \
    typing_extensions

WORKDIR /workspace
COPY . .
