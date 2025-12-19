# Dự Án Iris MLOps CI/CD Với GitHub Actions

## Ý Nghĩa Dự Án
Dự án này là một ví dụ thực hành về MLOps (Machine Learning Operations) sử dụng bộ dữ liệu Iris để xây dựng mô hình phân loại loài hoa. Mục đích chính là minh họa toàn bộ quy trình CI/CD (Continuous Integration/Continuous Deployment) từ phát triển mô hình đến triển khai Production, dựa trên tutorial AIO2025 MLOps CI/CD. Dự án giúp phá bỏ "Wall of Confusion" giữa team Development và Operations bằng cách tự động hóa huấn luyện mô hình, kiểm thử, build Docker image, và deploy lên cloud. 

Bộ dữ liệu Iris (từ scikit-learn) gồm 150 mẫu với 4 đặc trưng (sepal length, sepal width, petal length, petal width) để phân loại 3 loài hoa: setosa, versicolor, virginica. Dự án sử dụng mô hình Random Forest Classifier để dự đoán loài hoa với độ chính xác cao (~1.0), chứng minh cách áp dụng MLOps trong thực tế.

## Sơ Lược Output
Ứng dụng là một API FastAPI cho phép dự đoán loài hoa Iris. Input: JSON với 4 đặc trưng. Output: JSON với prediction (0-2), class_name ("setosa", "versicolor", "virginica"), và confidence (độ tin cậy, ví dụ 1.0).

## Các Step Thực Hiện Dự Án
Dưới đây là hướng dẫn từng bước để thiết lập và chạy dự án.

### Step 1: Tạo Repository Trên GitHub
- Đăng nhập GitHub (github.com).
- Nhấp "New repository" → Đặt tên "iris-mlops-cicd" → Chọn Public → Create repository.
- Link: https://github.com/huychuong0405/iris-mlops-cicd (thay username của bạn).

### Step 2: Tải Project Iris Về Máy Local
- Sử dụng link dữ liệu mẫu từ repo tham chiếu: https://github.com/undertanker86/iris-cicd-githubaction
- Clone về máy: Mở Terminal (macOS), chạy `git clone https://github.com/undertanker86/iris-cicd-githubaction.git`.
- Thư mục tải về gồm các file chính:
  - `train_model.py`: Huấn luyện mô hình Random Forest từ dữ liệu Iris, lưu artifact .pkl (ý nghĩa: Tạo mô hình để dự đoán từ 4 đặc trưng).
  - `app.py`: Xây dựng API FastAPI để load mô hình và dự đoán (ý nghĩa: Tạo endpoint /predict để người dùng gọi API).
  - `requirements.txt`: Liệt kê thư viện cần cài (scikit-learn, fastapi, uvicorn, pytest,...) (ý nghĩa: Tự động cài dependencies nhất quán).
  - `Dockerfile`: Công thức build Docker image (ý nghĩa: Đóng gói ứng dụng để chạy giống hệt mọi nơi).
  - `test_model.py`: Kiểm thử mô hình (accuracy, load, predict đúng) (ý nghĩa: Đảm bảo mô hình không lỗi).
  - `test_app.py`: Kiểm thử API (status code, format output) (ý nghĩa: Đảm bảo tích hợp mô hình-API ổn).
  - `.github/workflows/cicd.yml`: Cấu hình pipeline GitHub Actions (ý nghĩa: Tự động train/test/build/push khi push code).

- Sao chép các file này vào repo mới của bạn.

### Step 3: Upload Lên GitHub
- Trong Terminal, vào thư mục repo local: `cd iris-mlops-cicd`.
- Add file: `git add .`
- Commit: `git commit -m "Initial commit: Add Iris ML code and pipeline"`
- Push: `git push origin main` (sử dụng PAT nếu yêu cầu).

### Step 4: Link Với GitHub Actions (CI/CD)
- File `cicd.yml` đã cấu hình pipeline: Khi push code, GitHub Actions tự chạy trên cloud server GitHub (miễn phí).
- Các bước pipeline: Install dependencies → Train model → Run test → Build Docker image → Push lên Docker Hub.
- Kiểm tra: Tab Actions trên GitHub → Run success → Image mới trên Docker Hub.

### Step 5: Link Với Docker Hub
- Đăng ký Docker Hub (hub.docker.com).
- Tạo token access (Account Settings > Security > New Access Token, quyền Read/Write/Delete).
- Trong pipeline `cicd.yml`, dùng token để login và push image (tag latest + run number) lên repo `huychuong0405/iris-ml-api`.
- Kiểm tra: https://hub.docker.com/r/huychuong0405/iris-ml-api/tags.

### Step 6: Deploy On Production Bằng Render
- Đăng ký Render (dashboard.render.com, dùng GitHub login).
- New Web Service → Chọn repo GitHub → Render tự detect Dockerfile → Create (Free tier).
- Render pull image từ Docker Hub → deploy tự động → URL: https://iris-mlops-cicd.onrender.com.

## Góc Nhìn End User Trên Production
Người dùng cuối (end user) truy cập ứng dụng qua URL công khai (ví dụ: https://iris-mlops-cicd.onrender.com/docs) – đây là giao diện Swagger UI tự động.

- **Nhập gì**: Sử dụng POST /predict, input JSON với 4 đặc trưng (sepal_length, sepal_width, petal_length, petal_width). Ví dụ:
  ```json
  {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }
