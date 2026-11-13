"""
Script tạo bản xem trước (Preview) Bộ nhận diện thương hiệu Light Premium
Theo yêu cầu:
- Automotive Abstract: 3 dải khí động học + Vạch phân làn đỗ xe + Mũi xe mạ Champagne Gold
- Không dùng ảnh siêu xe 3D, không dùng chữ P đơn giản, không chói neon
- Xuất phiên bản nền sáng, phiên bản nền tối, icon 64x64, và logo ngang kết hợp tên app
- Lưu vào assets/branding/light_preview/ để trình duyệt trước khi thay thế logo chính
"""

import os
from PIL import Image, ImageDraw, ImageFont

GOC_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(GOC_PROJECT, "assets", "branding", "light_preview")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Bảng màu Light Premium chuẩn
TEAL_MAIN = (8, 127, 131, 255)       # #087F83
TEAL_LIGHT = (10, 150, 155, 255)     # #0A969B
TEAL_DARK = (6, 93, 96, 255)         # #065D60
GOLD_MAIN = (197, 164, 109, 255)     # #C5A46D
GOLD_LIGHT = (212, 182, 128, 255)    # #D4B680
TEXT_DARK = (22, 42, 53, 255)        # #162A35
TEXT_MUTED = (97, 116, 130, 255)     # #617482
BG_LIGHT = (243, 246, 248, 255)      # #F3F6F8
BG_DARK = (10, 15, 20, 255)          # #0A0F14
BORDER_LIGHT = (216, 225, 230, 255)  # #D8E1E6


def draw_automotive_abstract_shapes(draw: ImageDraw.ImageDraw, offset_x=0, offset_y=0, scale=1.0, is_dark=False):
    """Vẽ các đa giác Automotive Abstract theo tỷ lệ chuẩn."""
    def t(points):
        return [(int(p[0] * scale + offset_x), int(p[1] * scale + offset_y)) for p in points]

    teal_1 = TEAL_LIGHT if is_dark else TEAL_LIGHT
    teal_2 = (10, 150, 155, 255) if is_dark else TEAL_MAIN
    teal_3 = TEAL_MAIN if is_dark else TEAL_DARK
    gold_1 = GOLD_LIGHT if is_dark else GOLD_MAIN
    gold_2 = (224, 195, 146, 255) if is_dark else GOLD_LIGHT

    # Blade 1: Mui xe & Khí động học nóc (Roofline)
    p1 = [(140, 160), (330, 160), (410, 230), (365, 245), (305, 195), (155, 195)]
    draw.polygon(t(p1), fill=teal_1)

    # Blade 2: Thân xe & Vạch phân làn chính (Mid Body & Parking Bay)
    p2 = [(100, 245), (355, 245), (425, 305), (380, 320), (330, 280), (120, 280)]
    draw.polygon(t(p2), fill=teal_2)

    # Blade 3: Chân đế sàn đỗ & Làn dẫn đường (Ground Guidance Slot)
    p3 = [(140, 330), (320, 330), (365, 375), (325, 385), (295, 360), (160, 360)]
    draw.polygon(t(p3), fill=teal_3)

    # Accent Mũi xe mạ Champagne Gold (Aero Nose Cut)
    p_gold = [(365, 245), (410, 230), (425, 305), (380, 280)]
    draw.polygon(t(p_gold), fill=gold_1)

    # Điểm laser định vị thông minh (Smart Docking Laser Point)
    p_dot = [(440, 265), (455, 280), (440, 295), (425, 280)]
    draw.polygon(t(p_dot), fill=gold_2)


def tao_logo_light_512():
    """Tạo logo bản sáng 512x512 trong suốt và có nền xám nhạt."""
    # Bản trong suốt
    img_trans = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw_trans = ImageDraw.Draw(img_trans)
    draw_automotive_abstract_shapes(draw_trans, scale=1.0, is_dark=False)
    img_trans.save(os.path.join(OUTPUT_DIR, "logo_light_transparent.png"), "PNG")

    # Bản xem trước trên nền sáng #F3F6F8
    img_light = Image.new("RGBA", (512, 512), BG_LIGHT)
    draw_light = ImageDraw.Draw(img_light)
    draw_automotive_abstract_shapes(draw_light, scale=1.0, is_dark=False)
    img_light.save(os.path.join(OUTPUT_DIR, "preview_light_512.png"), "PNG")
    print("  [OK] Tạo preview_light_512.png")


def tao_logo_dark_512():
    """Tạo logo bản tối 512x512 xem trước."""
    img_dark = Image.new("RGBA", (512, 512), BG_DARK)
    draw_dark = ImageDraw.Draw(img_dark)
    draw_automotive_abstract_shapes(draw_dark, scale=1.0, is_dark=True)
    img_dark.save(os.path.join(OUTPUT_DIR, "preview_dark_512.png"), "PNG")
    print("  [OK] Tạo preview_dark_512.png")


def tao_logo_icon_64():
    """Tạo icon thu nhỏ kích thước 64x64."""
    img_64 = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw_64 = ImageDraw.Draw(img_64)
    # Scale 64/512 = 0.125
    draw_automotive_abstract_shapes(draw_64, scale=0.125, is_dark=False)
    img_64.save(os.path.join(OUTPUT_DIR, "preview_icon_64.png"), "PNG")
    print("  [OK] Tạo preview_icon_64.png")


def tao_logo_horizontal_light():
    """Tạo banner ngang kết hợp biểu tượng và tên ứng dụng 720x180."""
    w, h = 720, 180
    img_horiz = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img_horiz)

    # 1. Vẽ biểu tượng bên trái (scale ~ 0.3)
    draw_automotive_abstract_shapes(draw, offset_x=15, offset_y=12, scale=0.31, is_dark=False)

    # 2. Đường phân cách mỏng
    draw.line([(165, 30), (165, 150)], fill=BORDER_LIGHT, width=2)

    # 3. Vẽ chữ
    # Tìm font Segoe UI hoặc font mặc định
    try:
        font_main = ImageFont.truetype("segoeui.ttf", 36)
        font_sub = ImageFont.truetype("segoeui.ttf", 14)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((195, 50), "NEON PARKING", fill=TEXT_DARK, font=font_main)
    draw.text((198, 100), "SMART MANAGEMENT SYSTEM", fill=GOLD_MAIN, font=font_sub)

    img_horiz.save(os.path.join(OUTPUT_DIR, "preview_horizontal_light.png"), "PNG")
    print("  [OK] Tạo preview_horizontal_light.png")


def tao_logo_horizontal_dark():
    """Tạo banner ngang trên nền tối 720x180."""
    w, h = 720, 180
    img_horiz = Image.new("RGBA", (w, h), BG_DARK)
    draw = ImageDraw.Draw(img_horiz)

    draw_automotive_abstract_shapes(draw, offset_x=15, offset_y=12, scale=0.31, is_dark=True)
    draw.line([(165, 30), (165, 150)], fill=(40, 50, 65, 255), width=2)

    try:
        font_main = ImageFont.truetype("segoeui.ttf", 36)
        font_sub = ImageFont.truetype("segoeui.ttf", 14)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((195, 50), "NEON PARKING", fill=(255, 255, 255, 255), font=font_main)
    draw.text((198, 100), "SMART MANAGEMENT SYSTEM", fill=GOLD_LIGHT, font=font_sub)

    img_horiz.save(os.path.join(OUTPUT_DIR, "preview_horizontal_dark.png"), "PNG")
    print("  [OK] Tạo preview_horizontal_dark.png")


def main():
    print("=" * 60)
    print("  XUẤT CÁC BẢN XEM TRƯỚC (PREVIEW) LOGO LIGHT PREMIUM")
    print("=" * 60)
    tao_logo_light_512()
    tao_logo_dark_512()
    tao_logo_icon_64()
    tao_logo_horizontal_light()
    tao_logo_horizontal_dark()
    print("=" * 60)
    print(f"Hoàn tất! Các file đã lưu tại: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
