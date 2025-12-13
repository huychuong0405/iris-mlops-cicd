# Dockerfile – Đã fix lỗi build NumPy trên python:3.13-slim
FROM python:3.13-slim

# Cài các công cụ biên dịch cần thiết để build NumPy + scikit-learn từ source
# gcc, g++, make, build-essential, libgomp1… là bắt buộc
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements trước để tận dụng Docker layer cache
COPY requirements.txt .

# Cài dependencies (NumPy sẽ được build từ source nếu chưa có wheel)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir install -r requirements.txt

# Xóa công cụ build để giảm kích thước image cuối cùng (tùy chọn nhưng nên làm)
RUN apt-get purge -y --auto-remove build-essential g++ gcc make && \
    apt-get clean && \
    rm -rf /root/.cache/pip

# Copy toàn bộ source code
COPY src /app/src
COPY models /app/models   # nếu bạn có thư mục models chứa iris_model.pkl

# Expose port
EXPOSE 8000

# Chạy FastAPI bằng uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
