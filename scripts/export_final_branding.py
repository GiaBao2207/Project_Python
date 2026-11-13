"""
Xuất bộ nhận diện thương hiệu chính thức từ Phương án 3 (Negative Space Monogram):
- assets/branding/logo.svg (vector thực sự có thể chỉnh sửa)
- assets/branding/logo.png (512x512, nền trong suốt)
- assets/branding/logo_small.png (64x64, nền trong suốt)
- assets/branding/logo_horizontal.png (bản khóa ngang logo + chữ, nền trong suốt)
- assets/branding/app.ico (multi-size: 16, 24, 32, 48, 64, 128, 256)
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "assets", "branding")
os.makedirs(BRANDING_DIR, exist_ok=True)

# 1. Xuất file logo.svg chính thức
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="npmTealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00B4BC"/>
      <stop offset="100%" stop-color="#008C91"/>
    </linearGradient>
    <linearGradient id="npmGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E0C392"/>
      <stop offset="100%" stop-color="#C5A46D"/>
    </linearGradient>
  </defs>
  <!-- Trụ trái chữ N (Left Strut - Vạch phân ranh giới ô đỗ ngầm) -->
  <polygon points="120,120 185,120 135,392 70,392" fill="#006B70"/>
  
  <!-- Trụ phải chữ N (Right Strut) -->
  <polygon points="377,120 442,120 392,392 327,392" fill="url(#npmTealGrad)"/>
  
  <!-- Dải chéo khí động học liên kết chữ N (Dynamic Aero Blade) -->
  <polygon points="185,120 392,345 327,392 120,167" fill="#008C91"/>
  
  <!-- Vạch cắt âm bản mạ Champagne Gold (Negative Space Slot Divider) -->
  <polygon points="215,190 325,305 295,335 185,220" fill="url(#npmGoldGrad)"/>
  
  <!-- Vệt phản xạ ánh sáng kim loại công nghiệp -->
  <polygon points="120,120 185,120 175,135 110,135" fill="#E0C392"/>
</svg>'''

svg_path = os.path.join(BRANDING_DIR, "logo.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"[OK] Đã ghi {svg_path}")

# 2. Hàm vẽ Option 3 độ phân giải cao
SCALE = 4
def draw_option_3(draw, offset_x=0, offset_y=0, scale=1.0):
    c_teal_lo = "#006B70"
    c_teal_mid = "#008C91"
    c_teal_hi = "#00B4BC"
    c_gold = "#C5A46D"
    c_gold_hi = "#E0C392"

    def tr(pts):
        return [(offset_x + x * scale, offset_y + y * scale) for x, y in pts]

    draw.polygon(tr([(120, 120), (185, 120), (135, 392), (70, 392)]), fill=c_teal_lo)
    draw.polygon(tr([(377, 120), (442, 120), (392, 392), (327, 392)]), fill=c_teal_hi)
    draw.polygon(tr([(185, 120), (392, 345), (327, 392), (120, 167)]), fill=c_teal_mid)
    draw.polygon(tr([(215, 190), (325, 305), (295, 335), (185, 220)]), fill=c_gold)
    draw.polygon(tr([(120, 120), (185, 120), (175, 135), (110, 135)]), fill=c_gold_hi)

def render_logo(size=512):
    large_size = size * SCALE
    im = Image.new("RGBA", (large_size, large_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw_option_3(d, offset_x=0, offset_y=0, scale=(large_size / 512.0))
    return im.resize((size, size), Image.Resampling.LANCZOS)

# 3. Xuất logo.png (512x512)
logo_512 = render_logo(512)
logo_png_path = os.path.join(BRANDING_DIR, "logo.png")
logo_512.save(logo_png_path, "PNG")
print(f"[OK] Đã ghi {logo_png_path}")

# 4. Xuất logo_small.png (64x64)
logo_64 = render_logo(64)
logo_small_path = os.path.join(BRANDING_DIR, "logo_small.png")
logo_64.save(logo_small_path, "PNG")
print(f"[OK] Đã ghi {logo_small_path}")

# 5. Xuất app.ico (đa kích cỡ: 16, 24, 32, 48, 64, 128, 256)
ico_sizes = [16, 24, 32, 48, 64, 128, 256]
ico_images = [render_logo(s) for s in ico_sizes]
app_ico_path = os.path.join(BRANDING_DIR, "app.ico")
ico_images[-1].save(
    app_ico_path,
    format="ICO",
    sizes=[(s, s) for s in ico_sizes],
    append_images=ico_images[:-1]
)
print(f"[OK] Đã ghi {app_ico_path}")

# 6. Xuất logo_horizontal.png (khóa ngang cho Sidebar/Login: Icon + NEON PARKING MANAGER)
horiz_w = 400
horiz_h = 100
horiz_im = Image.new("RGBA", (horiz_w, horiz_h), (0, 0, 0, 0))
icon_part = render_logo(72)
horiz_im.paste(icon_part, (14, 14), icon_part)

d_h = ImageDraw.Draw(horiz_im)
try:
    font_main = ImageFont.truetype("segoeuib.ttf", 20)
    font_sub = ImageFont.truetype("segoeui.ttf", 10)
except Exception:
    font_main = font_sub = ImageFont.load_default()

d_h.text((98, 24), "NEON PARKING", fill="#F5F7FA", font=font_main)
d_h.text((100, 52), "MANAGER  •  SMART DESKTOP", fill="#C5A46D", font=font_sub)

horiz_path = os.path.join(BRANDING_DIR, "logo_horizontal.png")
horiz_im.save(horiz_path, "PNG")
print(f"[OK] Đã ghi {horiz_path}")

print("=== TOÀN BỘ ASSETS BRANDING CHÍNH THỨC ĐÃ ĐƯỢC XUẤT THÀNH CÔNG ===")
