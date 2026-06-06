# BÁO CÁO TIỂU LUẬN MÔN HỌC: MẠNG CẢM BIẾN
## Đề tài: Phân Loại Biển Báo Giao Thông Đường Bộ Việt Nam (TinyML - Edge Impulse)

**HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG**  
**CƠ SỞ TẠI THÀNH PHỐ HỒ CHÍ MINH**  

---

### THÔNG TIN CHUNG
*   **Giảng viên hướng dẫn:** ThS. Hồ Nhựt Minh
*   **Sinh viên thực hiện:** Nguyễn Đức Lương
*   **Mã số sinh viên:** N23DCCI044
*   **Lớp:** D23CQCI01-N

---

### 1. Giới thiệu đề tài
Tiểu luận tập trung nghiên cứu, thiết kế, xây dựng và huấn luyện mô hình học sâu nhúng (TinyML) trên nền tảng Edge Impulse nhằm phân loại bốn nhóm biển báo giao thông đường bộ cơ bản tại Việt Nam: **Biển báo cấm**, **Biển báo nguy hiểm**, **Biển chỉ dẫn** và **Biển hiệu lệnh**. Mô hình sau khi huấn luyện hướng tới khả năng triển khai trực tiếp trên các thiết bị phần cứng có tài nguyên giới hạn (RAM/Flash).

---

### 2. Cấu trúc thư mục và Mô tả mã nguồn dự án
*   `raw_sheets/`: Thư mục lưu trữ hình ảnh bảng biển báo giao thông gốc được thu thập từ quy chuẩn kỹ thuật quốc gia.
*   `base_crops/`: Thư mục chứa các ảnh biển báo đơn lẻ được cắt trích tự động từ ảnh gốc.
*   `dataset/`: Bộ dữ liệu hoàn chỉnh sau khi áp dụng các kỹ thuật tăng cường (Data Augmentation), được phân chia thành 4 lớp phục vụ huấn luyện: `cam`, `nguy_hiem`, `chi_dan`, `hieu_lenh` (mỗi lớp chứa 60 ảnh, tổng cộng 240 ảnh), sẵn sàng tải lên nền tảng Edge Impulse.
*   `data_segmentation_and_cleaning.py`: Chương trình xử lý ảnh sử dụng thư viện OpenCV để tự động nhận diện đường biên, cắt rời 140 biển báo từ bảng ảnh gốc.
*   `data_augmentation.py`: Chương trình tiền xử lý dữ liệu sử dụng thư viện Pillow và NumPy để thực hiện tẩy nền trắng bằng thuật toán Flood-fill, tạo độ trong suốt nền và tự động tăng cường dữ liệu ảnh (xoay góc, thay đổi tỉ lệ, điều chỉnh độ sáng, thêm nhiễu và ghép phông nền ngẫu nhiên) để nâng cao độ đa dạng cho tập dữ liệu.

---

### 3. Quy trình thực nghiệm và Hướng dẫn chạy mã nguồn

#### 3.1. Cài đặt các thư viện phụ thuộc:
Yêu cầu cài đặt các thư viện hỗ trợ xử lý ảnh và tính toán số học:
```bash
pip install opencv-python Pillow numpy
```

#### 3.2. Các bước triển khai thực nghiệm:

*   **Bước 1: Trích xuất và cắt rời các biển báo từ bảng ảnh thô**  
    Thực thi tệp tin mã nguồn sau để tự động phân đoạn hình ảnh:
    ```bash
    python data_segmentation_and_cleaning.py
    ```
    *Kết quả:* Các ảnh biển báo đơn lẻ được phân đoạn tự động và lưu trữ vào thư mục `base_crops/`.

*   **Bước 2: Xử lý xóa nền và tăng cường hình ảnh để sinh bộ dữ liệu mẫu**  
    Thực thi chương trình tăng cường dữ liệu:
    ```bash
    python data_augmentation.py
    ```
    *Kết quả:* Sinh ra tập dữ liệu huấn luyện chuẩn hóa gồm 240 ảnh (đã được xóa nền, xoay nghiêng, ghép phông nền môi trường thực tế ngẫu nhiên) tại thư mục `dataset/`. Thư mục này được sử dụng để nén hoặc tải trực tiếp lên dự án Edge Impulse Studio.

---

### 4. Kết quả thực nghiệm và Đánh giá hiệu năng trên Edge Impulse
Báo cáo tóm tắt kết quả huấn luyện mô hình MobileNetV2 và các thông số đánh giá hiệu năng thu được từ Edge Impulse:

*   **Kiến trúc mạng áp dụng:** MobileNetV2 160x160 (hệ số co giãn alpha = 0.5)
*   **Độ chính xác của mô hình (Accuracy):** 89.7%
*   **Giá trị độ hao hụt (Loss value):** 0.28
*   **Điểm số F1 trung bình có trọng số (Weighted average F1 score):** 89% (0.89)
*   **Đánh giá hiệu năng trên thiết bị nhúng thực tế (On-device performance):**
    *   **Thời gian suy luận (Inferencing time):** 334 ms
    *   **Dung lượng RAM đỉnh (Peak RAM usage):** 507.8 KB
    *   **Dung lượng bộ nhớ Flash yêu cầu (Flash usage):** 2.8 MB
    *   **Trình biên dịch tối ưu hóa:** EON Compiler (Cấu hình RAM optimized)
