# HƯỚNG DẪN BỘ NHẬN DIỆN THƯƠNG HIỆU LIGHT PREMIUM (BRANDING_DESIGN_GUIDE)

> **Dự án**: Neon Parking Manager  
> **Phong cách**: Light Premium Automotive Management  
> **Định hướng**: Tối giản, hiện đại, sang trọng, đẳng cấp công nghiệp (Industrial Luxury)  
> **Trạng thái**: **BẢN XEM TRƯỚC (PREVIEW) – ĐANG CHỜ PHÊ DUYỆT CỦA NGƯỜI DÙNG**

---

## 1. TRIẾT LÝ VÀ Ý TƯỞNG THIẾT KẾ BIỂU TƯỢNG (AUTOMOTIVE ABSTRACT)

Logo được xây dựng dựa trên sự hòa quyện giữa **Ngôn ngữ Khí động học Ô tô (Aerodynamics)** và **Cấu trúc Làn đỗ xe Thông minh (Smart Parking Bay)**:

```text
       [Mui lướt gió khí động học - Roofline]  ─────────┐
                                                       ├─► 3 Lưỡi khí động học (Aero Blades)
  [Thân xe & Vạch phân làn đỗ - Main Bay Slot] ─────────┤   Cắt vát 30° thể hiện tốc độ,
                                                       │   dòng xe di chuyển mượt mà
[Chân đế sàn đỗ hướng dẫn - Guidance Base]   ─────────┘

  [Aero Nose Cut] ──► Mũi xe cắt mạ Champagne Gold (#C5A46D): Điểm nhấn sang trọng
  [Laser Diamond] ──► Điểm định vị laser thông minh: Công nghệ tự động hóa bãi xe
```

### Các nguyên tắc đã tuân thủ nghiêm ngặt:
- **KHÔNG dùng chữ P đơn giản**: Tránh sự nhàm chán như biển báo giao thông công cộng.
- **KHÔNG dùng ảnh siêu xe 3D**: Tránh lỗi thời, nhòe vỡ nét khi thu nhỏ kích thước.
- **KHÔNG lạm dụng neon chói**: Sử dụng Primary Teal `#087F83` và Champagne Gold `#C5A46D` trầm ấm, cao cấp.
- **Có đầy đủ phiên bản**: Nền sáng, nền tối, icon nhỏ 64px và bản logo ngang kết hợp tên thương hiệu.
- **Định dạng SVG vector**: Độ phân giải vô hạn, có thể chỉnh sửa và in ấn báo cáo chất lượng cao.

---

## 2. DANH MỤC CÁC TỆP XEM TRƯỚC TẠI THƯ MỤC `assets/branding/light_preview/`

| Tên tệp | Định dạng | Kích thước | Mục đích sử dụng |
| :--- | :---: | :---: | :--- |
| `logo_abstract_light.svg` | SVG | Vector 512x512 | Logo vector gốc cho tài liệu in ấn và giao diện nền sáng |
| `logo_horizontal_light.svg`| SVG | Vector 720x180 | Logo dạng ngang kết hợp biểu tượng và tên ứng dụng nền sáng |
| `logo_abstract_dark.svg`  | SVG | Vector 512x512 | Biểu tượng vector trên nền tối |
| `preview_light_512.png`    | PNG | 512x512 | Bản xem trước biểu tượng trên nền sáng `#F3F6F8` |
| `preview_dark_512.png`     | PNG | 512x512 | Bản xem trước biểu tượng trên nền tối `#0A0F14` |
| `preview_icon_64.png`      | PNG | 64x64 | Bản xem trước icon ứng dụng ở kích thước nhỏ |
| `preview_horizontal_light.png` | PNG | 720x180 | Bản xem trước logo ngang trên nền sáng |
| `preview_horizontal_dark.png`  | PNG | 720x180 | Bản xem trước logo ngang trên nền tối |

---

## 3. THÔNG SỐ BẢNG MÀU THƯƠNG HIỆU

| Tên màu | Mã HEX | Mã RGB | Ứng dụng trong thiết kế |
| :--- | :---: | :---: | :--- |
| **Primary Teal** | `#087F83` | `(8, 127, 131)` | Dải thân xe và vạch phân làn trung tâm, nút bấm chính |
| **Teal Light** | `#0A969B` | `(10, 150, 155)` | Dải mui xe phía trên |
| **Teal Dark** | `#065D60` | `(6, 93, 96)` | Chân đế sàn đỗ phía dưới |
| **Champagne Gold** | `#C5A46D` | `(197, 164, 109)` | Điểm nhấn mũi xe và điểm laser định vị |
| **Main Text** | `#162A35` | `(22, 42, 53)` | Chữ thương hiệu chính `NEON PARKING` |
| **Background Light** | `#F3F6F8` | `(243, 246, 248)` | Màu nền ứng dụng và nền card xem trước |

---

## 4. QUY TRÌNH THAY THẾ KHI ĐƯỢC PHÊ DUYỆT

Khi người dùng duyệt thiết kế logo này:
1. Sao chép `logo_abstract_light.svg` thành `assets/branding/logo.svg`.
2. Sao chép `logo_light_transparent.png` thành `assets/branding/logo.png`.
3. Sao chép `preview_icon_64.png` thành `assets/branding/logo_small.png`.
4. Tạo file `assets/branding/app.ico` đồng bộ.
Ứng dụng sẽ tự động áp dụng biểu tượng mới trên toàn bộ các màn hình thông qua `gui/components/branding.py`.
