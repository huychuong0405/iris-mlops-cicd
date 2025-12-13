# Dockerfile – Đã fix hoàn toàn lỗi COPY và build NumPy trên python:3.13-slim
FROM python:3.13-slim

# Cài công cụ biên dịch cần thiết để build NumPy/scikit-learn nếu không có wheel
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        make \
        libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements trước để tận dụng cache layer
COPY requirements.txt .

# Upgrade pip và cài dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Dọn dẹp công cụ build để giảm kích thước image
RUN apt-get purge -y --auto-remove build-essential gcc g++ make && \
    apt-get clean && \
    rm -rf /root/.cache/pip

# Copy source code
COPY src /app/src

# Expose port cho FastAPI
EXPOSE 8000

# Chạy ứng dụng
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
