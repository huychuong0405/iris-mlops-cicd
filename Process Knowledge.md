
### File 2: Tổng Hợp Kiến Thức Dự Án Iris MLOps – Các Team, File, Và Quy Trình

#### Các Team Liên Quan Trong Từng Môi Trường Và Vai Trò
Dự án Iris MLOps được chia thành các team theo mô hình DevOps/MLOps, với mục tiêu tự động hóa để phá bỏ "Wall of Confusion" (trang 1-2). Mỗi team làm việc ở môi trường phù hợp, liên kết qua GitHub để chuyển giao code.

- **Team AI/ML – Vai trò ở Môi Trường Dev**: Xây dựng mô hình ML cốt lõi. Huấn luyện Random Forest từ bộ dữ liệu Iris (150 mẫu, 4 đặc trưng: sepal length/width, petal length/width) để phân loại 3 loài hoa (setosa, versicolor, virginica). Output: File mô hình .pkl với accuracy ~1.0. Liên kết: Commit code lên GitHub để team Backend tích hợp.

- **Team Backend – Vai trò ở Môi Trường Dev & Integration**: Tích hợp mô hình vào API FastAPI. Load .pkl từ team AI/ML, tạo endpoint /predict nhận input JSON 4 đặc trưng, chạy dự đoán. Output: API trả JSON (prediction, class_name, confidence). Liên kết: Kết nối với team QC để test, commit GitHub để DevOps automate.

- **Team QC – Vai trò ở Môi Trường Staging & UAT**: Kiểm tra chất lượng. Viết test cho mô hình (accuracy >0.9, predict đúng) và API (status code, format output). Output: Báo cáo test passed (6 cases). Liên kết: Nếu fail, quay lại Dev; nếu OK, chuyển DevOps deploy.

- **Team DevOps – Vai trò Xuyên Suốt Từ Integration Đến Production**: Tự động hóa pipeline. Viết cicd.yml và Dockerfile để khi push code → tự train/test/build/push Docker. Output: Image Docker sẵn sàng deploy. Liên kết: Nhận code từ tất cả team qua GitHub, deploy Production trên Render.

#### Output Các File Của Từng Team
- **Team AI/ML**: `train_model.py` (output: iris_model.pkl – mô hình đã train).
- **Team Backend**: `app.py` (output: API FastAPI), `requirements.txt` (list thư viện).
- **Team QC**: `test_model.py` (test mô hình), `test_app.py` (test API).
- **Team DevOps**: `cicd.yml` (pipeline config), `Dockerfile` (image build), image Docker trên Hub.

#### Mục Đích, Ý Nghĩa Từng File Theo Trình Tự Chi Tiết, Cách Hoạt Động
Trình tự theo flow: Từ train → API → test → pipeline → deploy. Mỗi file hoạt động như một bộ phận trong dây chuyền.

1. **train_model.py (Team AI/ML, Môi Trường Dev)**:
   - **Mục đích/Ý nghĩa**: Huấn luyện mô hình từ 4 features (sepal/petal length/width) để dự đoán loài hoa Iris (3 lớp). Ý nghĩa: Tạo "bộ não" dự đoán chính xác cao (~1.0), tái lập được (random_state=42).
   - **Cách hoạt động**: Load dữ liệu Iris từ scikit-learn, split train/test, fit Random Forest (n_estimators=100), lưu .pkl bằng joblib. Output: File .pkl chứa mô hình đã học.

2. **app.py (Team Backend, Dev & Integration)**:
   - **Mục đích/Ý nghĩa**: Tạo API FastAPI để load .pkl và predict. Ý nghĩa: Biến mô hình thành dịch vụ web, người dùng gửi input nhận output mà không cần biết ML.
   - **Cách hoạt động**: Load model từ .pkl (hoặc train mới nếu thiếu), endpoint /predict nhận JSON 4 features, chạy model.predict() → trả JSON (prediction, class_name, confidence).

3. **requirements.txt (Team Backend/DevOps, Dev)**:
   - **Mục đích/Ý nghĩa**: Liệt kê thư viện (scikit-learn, fastapi...). Ý nghĩa: Tự động cài nhất quán ở mọi môi trường, tránh lỗi dependencies.
   - **Cách hoạt động**: Lệnh `pip install -r requirements.txt` cài hết gói với phiên bản cố định.

4. **test_model.py (Team QC, Staging)**:
   - **Mục đích/Ý nghĩa**: Test riêng mô hình (accuracy >0.9, predict đúng). Ý nghĩa: Đảm bảo mô hình không lỗi trước khi tích hợp.
   - **Cách hoạt động**: Load .pkl, chạy pytest với 4-6 cases (ví dụ: test_model_accuracy_threshold kiểm tra accuracy).

5. **test_app.py (Team QC, Staging & UAT)**:
   - **Mục đích/Ý nghĩa**: Test API (status code, output format). Ý nghĩa: Kiểm tra tích hợp model-API, xử lý lỗi input.
   - **Cách hoạt động**: Chạy pytest với httpx để gọi endpoint /predict, kiểm tra JSON trả về đúng.

6. **cicd.yml (Team DevOps, Integration → Production)**:
   - **Mục đích/Ý nghĩa**: Cấu hình pipeline GitHub Actions. Ý nghĩa: Tự động train/test/build/push khi push code, tránh thủ công.
   - **Cách hoạt động**: Trigger on push → chạy steps: install dependencies, train, test, login Docker, build/push image.

7. **Dockerfile (Team DevOps, Integration → Production)**:
   - **Mục đích/Ý nghĩa**: Đóng gói app thành Docker image. Ý nghĩa: Chạy giống hệt mọi nơi, không phụ thuộc máy chủ.
   - **Cách hoạt động**: FROM python:3.11-slim → COPY code/thư viện → RUN pip install → CMD chạy uvicorn.

#### Tại Sao Upload Các File Lên GitHub?
- GitHub là “kho trung tâm” lưu code của tất cả team → dễ chia sẻ, review, và version control (xem lịch sử sửa).
- Trigger CI/CD tự động (cicd.yml chạy khi push).
- Không upload → không có pipeline → phải làm thủ công → chậm, dễ lỗi, không liên kết team.

