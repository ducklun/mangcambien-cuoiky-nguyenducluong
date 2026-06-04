# Phân Loại Biển Báo Giao Thông Đường Bộ Việt Nam (TinyML - Edge Impulse)

Tiểu luận thực hiện thiết kế, xây dựng và huấn luyện mô hình học sâu nhúng (TinyML) trên nền tảng Edge Impulse nhằm phân loại bốn nhóm biển báo giao thông đường bộ cơ bản tại Việt Nam: **Biển báo cấm**, **Biển báo nguy hiểm**, **Biển chỉ dẫn** và **Biển hiệu lệnh**.

## 1. Thành viên nhóm thực hiện
*   **Họ và tên:** Nguyễn Đức Lương
*   **MSSV:** N23DCCI044
*   **Lớp:** D23CQCI01-N
*   **Học viện:** Học viện Công nghệ Bưu chính Viễn thông Cơ sở tại TP. Hồ Chí Minh
*   **GVHD:** Hồ Nhựt Minh

---

## 2. Cấu trúc thư mục dự án
*   `raw_sheets/`: Chứa 4 ảnh bảng biển báo giao thông gốc thu thập từ tài liệu chuẩn.
*   `base_crops/`: Chứa các biển báo riêng lẻ được chương trình cắt tự động từ ảnh gốc.
*   `dataset/`: Bộ dữ liệu đã tăng cường (Data Augmentation) chia thành 4 lớp (`cam`, `nguy_hiem`, `chi_dan`, `hieu_lenh`), mỗi lớp có 60 ảnh (tổng cộng 240 ảnh) dùng để nạp lên Edge Impulse.
*   `data_segmentation_and_cleaning.py`: Lập trình OpenCV để tự động nhận diện đường biên, cắt rời 140 biển báo thô từ bảng ảnh gốc.
*   `data_augmentation.py`: Lập trình Pillow và numpy để tẩy nền trắng bằng thuật toán Flood-fill, tạo độ trong suốt nền và tự động tăng cường dữ liệu ảnh (xoay, tỉ lệ, ánh sáng, nhiễu, ghép phông nền ngẫu nhiên).

---

## 3. Hướng dẫn cài đặt và chạy mã nguồn

### Yêu cầu cài đặt thư viện phụ thuộc:
```bash
pip install opencv-python Pillow numpy
```

### Bước 1: Chạy cắt tách biển báo từ ảnh bảng thô
```bash
python data_segmentation_and_cleaning.py
```
*Kết quả:* Các ảnh biển báo riêng lẻ sẽ được cắt tự động và lưu vào thư mục `base_crops/`.

### Bước 2: Chạy tẩy nền và tăng cường dữ liệu để sinh bộ dataset
```bash
python data_augmentation.py
```
*Kết quả:* Bộ dữ liệu 240 ảnh hoàn chỉnh (đã tẩy nền, xoay nghiêng, ghép phông nền hỗn hợp và giả lập môi trường thực tế) sẽ được lưu vào thư mục `dataset/`. Bạn chỉ cần nén hoặc tải trực tiếp thư mục này lên Edge Impulse Studio.

---

## 4. Kết quả huấn luyện trên Edge Impulse
*   **Kiến trúc mạng:** MobileNetV2 160x160 (hệ số alpha là 0.5)
*   **Độ chính xác (Accuracy):** 89.7%
*   **Giá trị Loss:** 0.28
*   **Weighted average F1 score:** 89% (0.89)
*   **Hiệu năng trên thiết bị thực tế (On-device performance):**
    *   Thời gian suy luận (Inferencing time): 334 ms
    *   Dung lượng RAM tối đa (Peak RAM usage): 507.8 KB
    *   Dung lượng bộ nhớ Flash yêu cầu: 2.8 MB
    *   Trình biên dịch tối ưu: EON Compiler (RAM optimized)
