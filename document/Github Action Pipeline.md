# Quy Trình Chạy Chi Tiết Của GitHub Actions Pipeline (CI/CD) Trong Dự Án Iris MLOps

## Tổng Quan
Pipeline GitHub Actions trong dự án này được định nghĩa hoàn toàn bởi file **`.github/workflows/cicd.yml`**.  
Khi có sự kiện `push` lên branch `main` (hoặc `develop`), GitHub sẽ tự động khởi động một **run mới** trên cloud server của mình và thực hiện tuần tự các bước được khai báo trong file YAML này.

GitHub Actions không cần server riêng – mọi thứ chạy trên **máy ảo tạm thời (runner)** do GitHub cung cấp miễn phí (ubuntu-latest).

## Quy Trình Chạy Chi Tiết (Theo Thứ Tự Trong cicd.yml)

| Thứ Tự | Step Trong YAML                          | Mô Tả Chi Tiết                                                                 | Máy Chủ Thực Thi                  | Ý Nghĩa Trong Dự Án Iris                          |
|--------|------------------------------------------|--------------------------------------------------------------------------------|-----------------------------------|---------------------------------------------------|
| 1      | `Checkout Code` (`actions/checkout@v4`)  | GitHub clone toàn bộ repo (tất cả file code) vào máy ảo cloud.                 | Cloud GitHub (ubuntu-latest)      | Lấy code mới nhất từ repo của bạn.                |
| 2      | `Set up Python` (`actions/setup-python@v5`) | Cài đặt Python phiên bản 3.11 trên máy ảo.                                     | Cloud GitHub                      | Chuẩn bị môi trường Python giống local.           |
| 3      | `Install Dependencies`                   | Chạy lệnh `pip install -r requirements.txt` → cài tất cả thư viện (scikit-learn, fastapi, uvicorn, pytest...). | Cloud GitHub                      | Đảm bảo mọi thư viện cần thiết được cài tự động.  |
| 4      | `Train ML Model`                         | Chạy `python src/train_model.py` → huấn luyện lại mô hình Random Forest từ dữ liệu Iris → lưu `iris_model.pkl`. | Cloud GitHub                      | Đảm bảo mô hình luôn mới và tái lập được.         |
| 5      | `Test Model`                             | Chạy `pytest tests/test_model.py` → kiểm tra 4-6 test cases về mô hình (accuracy, load, predict đúng). | Cloud GitHub                      | Nếu fail → dừng pipeline → tránh lỗi ở Production. |
| 6      | `Test API`                               | Chạy `pytest tests/test_app.py` → kiểm tra API trả kết quả đúng, format JSON, xử lý lỗi. | Cloud GitHub                      | Kiểm tra tích hợp model + API.                    |
| 7      | `Set up Docker Buildx`                   | Chuẩn bị công cụ Docker Buildx để build image hiệu quả.                         | Cloud GitHub                      | Sẵn sàng build container.                         |
| 8      | `Login to Docker Hub`                    | Đăng nhập Docker Hub bằng username + token (hardcoded hoặc secrets).           | Cloud GitHub                      | Chuẩn bị push image lên kho lưu trữ.              |
| 9      | `Build and Push Docker Image`            | Build image từ `Dockerfile` → push lên Docker Hub với tag `latest` và số run.  | Cloud GitHub                      | Tạo container hoàn chỉnh để deploy Production.   |
| 10     | `Image digest` & `Cleanup`               | In thông báo thành công và dọn dẹp file tạm.                                    | Cloud GitHub                      | Hoàn tất pipeline sạch sẽ.                        |

## Khi Pipeline Hoàn Thành
- Nếu tất cả step xanh lá → **success** → Docker image mới được push lên Docker Hub.
- Render (Production) tự động pull image mới nhất → redeploy → ứng dụng live với code mới.
- Nếu có step đỏ (fail) → pipeline dừng → không deploy → team sửa code → push lại → rerun tự động.

## Tại Sao Toàn Bộ Flow Được Tạo Từ cicd.yml?
- File YAML này là **"kịch bản tự động"** – mỗi `step` là một lệnh hoặc action (từ marketplace GitHub).
- GitHub đọc file này → biết chính xác phải làm gì khi có push.
- Không cần viết code Python riêng để tự động hóa → chỉ cần YAML dễ đọc, dễ chỉnh sửa.

## Lợi Ích Của Việc Chạy Trên Cloud GitHub
- Miễn phí (2000 phút/tháng cho repo public).
- Máy ảo sạch mỗi lần → không bị ảnh hưởng môi trường cũ.
- Tự động, nhanh, không cần server riêng.
- Dễ theo dõi log trên tab Actions.

File này có thể đặt trong thư mục gốc repo hoặc trong `docs/` với tên `GITHUB_ACTIONS_PIPELINE.md` để team dễ đọc.
