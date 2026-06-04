# -*- coding: utf-8 -*-
import cv2
import os
import random
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

crops_dir = "base_crops"
dataset_dir = "dataset"
classes = ["cam", "nguy_hiem", "chi_dan", "hieu_lenh"]

for cls in classes:
    os.makedirs(os.path.join(dataset_dir, cls), exist_ok=True)

# Hàm tẩy nền trắng thô bên ngoài thành trong suốt (Transparent)
def clean_background(img_path):
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        return None
    h, w, c = img_bgr.shape
    
    # Sử dụng bản sao BGR 3 kênh để loang màu (floodFill)
    img_fill = img_bgr.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # Loang màu bắt đầu từ 4 góc ảnh
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    for x, y in corners:
        pixel = img_bgr[y, x]
        if int(pixel[0]) + int(pixel[1]) + int(pixel[2]) > 600: # Gần màu trắng
            cv2.floodFill(img_fill, mask, (x, y), (0, 0, 0), (25, 25, 25), (25, 25, 25), flags=8 | (1 << 8))
            
    # Chuyển ảnh gốc sang BGRA (4 kênh màu)
    img_bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
    sub_mask = mask[1:h+1, 1:w+1]
    img_bgra[sub_mask == 1, 3] = 0 # Đặt kênh Alpha = 0 (trong suốt) cho nền
    
    # Cắt xén bớt 2 pixel ngoài rìa để loại bỏ hoàn toàn viền trắng răng cưa
    if h > 10 and w > 10:
        img_bgra = img_bgra[2:h-2, 2:w-2]
        
    img_rgba = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2RGBA)
    return Image.fromarray(img_rgba)

# Hàm sinh hình nền hỗn hợp ngẫu nhiên để mô phỏng môi trường nhiễu vật lý
def generate_random_background():
    bg = Image.new("RGB", (300, 300))
    draw = ImageDraw.Draw(bg)
    r_base = random.randint(80, 220)
    g_base = random.randint(80, 220)
    b_base = random.randint(80, 220)
    draw.rectangle([0, 0, 300, 300], fill=(r_base, g_base, b_base))
    
    for _ in range(random.randint(4, 10)):
        x1 = random.randint(0, 250)
        y1 = random.randint(0, 250)
        x2 = x1 + random.randint(40, 160)
        y2 = y1 + random.randint(40, 160)
        fill_color = (
            max(0, min(255, r_base + random.randint(-45, 45))),
            max(0, min(255, g_base + random.randint(-45, 45))),
            max(0, min(255, b_base + random.randint(-45, 45)))
        )
        draw.rectangle([x1, y1, x2, y2], fill=fill_color)
    return bg

# Hàm thực hiện các phép tăng cường dữ liệu và ghép đè
def augment_sign(base_img, filename, output_path):
    # 1. Thay đổi kích thước ngẫu nhiên (simulating distance)
    scale_factor = random.uniform(0.45, 0.8)
    new_size = int(200 * scale_factor)
    img_temp = base_img.copy().resize((new_size, new_size), Image.Resampling.LANCZOS)
    
    # 2. Xoay góc ngẫu nhiên (simulating tilt)
    angle = random.uniform(-20, 20)
    img_temp = img_temp.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    # 3. Tạo nền ngẫu nhiên
    bg = generate_random_background()
    
    # 4. Ghép đè biển báo lên nền
    max_offset_x = bg.width - img_temp.width
    max_offset_y = bg.height - img_temp.height
    offset_x = random.randint(0, max_offset_x) if max_offset_x > 0 else 0
    offset_y = random.randint(0, max_offset_y) if max_offset_y > 0 else 0
    
    bg.paste(img_temp, (offset_x, offset_y), img_temp)
    final_img = bg.convert("RGB")
    
    # 5. Điều chỉnh ngẫu nhiên độ sáng, độ tương phản và màu sắc
    final_img = ImageEnhance.Brightness(final_img).enhance(random.uniform(0.7, 1.3))
    final_img = ImageEnhance.Contrast(final_img).enhance(random.uniform(0.75, 1.25))
    final_img = ImageEnhance.Color(final_img).enhance(random.uniform(0.6, 1.4))
    
    # 6. Làm mờ nhẹ ngẫu nhiên (simulating motion blur/out-of-focus)
    if random.random() < 0.3:
        final_img = final_img.filter(ImageFilter.GaussianBlur(random.uniform(0.5, 1.5)))
        
    # 7. Thêm nhiễu hạt ngẫu nhiên (simulating webcam noise)
    if random.random() < 0.4:
        img_arr = np.array(final_img, dtype=np.float32)
        noise = np.random.normal(0, random.uniform(4, 10), img_arr.shape)
        img_arr = np.clip(img_arr + noise, 0, 255).astype(np.uint8)
        final_img = Image.fromarray(img_arr)
        
    final_img.save(os.path.join(output_path, filename), "JPEG", quality=90)

print("=== BẮT ĐẦU TĂNG CƯỜNG DỮ LIỆU ===")
for cls in classes:
    output_folder = os.path.join(dataset_dir, cls)
    for f in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, f))
        
    cls_crops_dir = os.path.join(crops_dir, cls)
    crop_files = [os.path.join(cls_crops_dir, f) for f in os.listdir(cls_crops_dir) if f.endswith(".png")]
    
    # Khử nền cho các ảnh cắt thô
    base_images = []
    for file_path in crop_files:
        cleaned_img = clean_background(file_path)
        if cleaned_img is not None:
            base_images.append(cleaned_img)
            
    print(f"Nhóm '{cls}': Cắt sạch được {len(base_images)} ảnh gốc. Đang sinh 60 ảnh tăng cường...")
    for i in range(60):
        base_img = random.choice(base_images)
        filename = f"sign_{i+1:03d}.jpg"
        augment_sign(base_img, filename, output_folder)

print("=== TĂNG CƯỜNG DỮ LIỆU HOÀN TẤT ===")
