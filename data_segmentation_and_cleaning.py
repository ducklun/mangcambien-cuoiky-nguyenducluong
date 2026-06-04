# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np

# Thư mục chứa các ảnh bảng biển báo thô
raw_dir = "raw_sheets"
crops_dir = "base_crops"
os.makedirs(crops_dir, exist_ok=True)

images = {
    "chi_dan": os.path.join(raw_dir, "chi_dan.jpg"),
    "hieu_lenh": os.path.join(raw_dir, "hieu_lenh.jpg"),
    "nguy_hiem": os.path.join(raw_dir, "nguy_hiem.jpg"),
    "cam": os.path.join(raw_dir, "cam.jpg")
}

print("=== BẮT ĐẦU PHÂN TÁCH VÀ CẮT BIỂN BÁO ===")

for key, img_path in images.items():
    if not os.path.exists(img_path):
        print(f"Lỗi: Không tìm thấy file {img_path}")
        continue
        
    print(f"Đang xử lý nhóm: {key}...")
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Nhị phân hóa đảo ngược: nền trắng (~255) chuyển thành đen (0), biển báo thành trắng (255)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Loại bỏ nhiễu nhỏ bằng toán tử mở (Morphological Open)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # Tìm kiếm các đường biên bên ngoài (external contours)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    count = 0
    save_folder = os.path.join(crops_dir, key)
    os.makedirs(save_folder, exist_ok=True)
    
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = float(w) / h
        area = cv2.contourArea(c)
        
        # Lọc các contour có kích thước và hình dáng vuông vức phù hợp với biển báo
        if 25 < w < 200 and 25 < h < 200 and 0.75 < aspect_ratio < 1.35 and area > 400:
            crop = img[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(save_folder, f"crop_{count}.png"), crop)
            count += 1
            
    print(f"-> Đã lưu {count} biển báo sạch vào thư mục: {save_folder}")

print("=== PHÂN TÁCH HOÀN TẤT ===")
