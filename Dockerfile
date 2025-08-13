# 使用官方 NVIDIA CUDA 映像檔作為基礎
FROM nvidia/cuda:11.6.2-cudnn8-devel-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Taipei

# 設定工作目錄
WORKDIR /app

# 更新 apt-get 並安裝 Python 和 pip
RUN apt-get update && \
    apt-get install -y tzdata python3 python3-pip openjdk-11-jre-headless && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# 將您的專案檔案複製到容器中
# 這會將 /workspace 的內容複製到容器的 /app 目錄
COPY . .

# 安裝 Python 相依套件
RUN pip3 install pandas numpy scikit-learn "tensorflow==2.13.1"