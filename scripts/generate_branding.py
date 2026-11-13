"""
Script tạo bộ nhận diện thương hiệu NEON PARKING MANAGER
Tạo logo.svg, logo.png (512x512), logo_small.png (64x64), app.ico
Phong cách Cyberpunk Futuristic: Khiên bảo vệ + Chữ P phát sáng + Siêu xe thể thao góc cạnh Neon
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "branding")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Tạo file logo.svg chất lượng vector cao
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Gradients -->
    <linearGradient id="cyberShieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="50%" stop-color="#7928CA" />
      <stop offset="100%" stop-color="#FF007F" />
    </linearGradient>
    <linearGradient id="carBodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1A1F35" />
      <stop offset="100%" stop-color="#0D0F18" />
    </linearGradient>
    <linearGradient id="neonCyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="100%" stop-color="#70FFFF" />
    </linearGradient>
    <linearGradient id="neonPink" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF007F" />
      <stop offset="100%" stop-color="#FF66B2" />
    </linearGradient>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Khối khiên ngoài Cyberpunk (Shield Frame) -->
  <polygon points="256,28 460,110 460,350 256,484 52,350 52,110" 
           fill="#151928" fill-opacity="0.85" 
           stroke="url(#cyberShieldGrad)" stroke-width="8" stroke-linejoin="round"/>

  <!-- Viền khiên trong góc cạnh -->
  <polygon points="256,48 436,122 436,336 256,456 76,336 76,122" 
           fill="none" 
           stroke="#00F0FF" stroke-width="2" stroke-opacity="0.4" stroke-dasharray="12,6"/>

  <!-- Thân xe Cyberpunk góc cạnh phía dưới (Futuristic Sports Car Silhouette) -->
  <!-- Kính chắn gió xe -->
  <polygon points="256,150 330,225 182,225" 
           fill="#00F0FF" fill-opacity="0.18" 
           stroke="#00F0FF" stroke-width="3" stroke-linejoin="round"/>

  <!-- Nắp capo và vòm xe -->
  <polygon points="182,225 330,225 385,275 365,335 147,335 127,275" 
           fill="url(#carBodyGrad)" 
           stroke="url(#cyberShieldGrad)" stroke-width="4" stroke-linejoin="round"/>

  <!-- Đèn pha xe Neon Cyan sắc bén -->
  <polygon points="140,285 175,285 190,295 130,295" fill="#00F0FF" filter="url(#neonGlow)"/>
  <polygon points="372,285 337,285 322,295 382,295" fill="#00F0FF" filter="url(#neonGlow)"/>

  <!-- Hốc hút gió trung tâm xe -->
  <polygon points="220,305 292,305 282,325 230,325" fill="#FF007F" fill-opacity="0.6"/>

  <!-- Đèn gầm neon pink -->
  <line x1="150" y1="345" x2="362" y2="345" stroke="#FF007F" stroke-width="5" stroke-linecap="round" filter="url(#neonGlow)"/>

  <!-- Biểu tượng chữ P (PARKING) NEON TỎA SÁNG VƯỢT LÊN TRUNG TÂM -->
  <!-- Thân đứng chữ P -->
  <rect x="226" y="90" width="18" height="110" rx="4" fill="url(#neonCyan)" filter="url(#neonGlow)"/>
  <!-- Vòng cong chữ P -->
  <path d="M 238,90 H 280 C 310,90 310,145 280,145 H 238 Z" 
        fill="none" stroke="url(#neonPink)" stroke-width="18" stroke-linejoin="round" stroke-linecap="round" filter="url(#neonGlow)"/>

  <!-- Vi mạch công nghệ trang trí ở 2 cánh khiên -->
  <circle cx="85" cy="130" r="5" fill="#00F0FF"/>
  <line x1="85" y1="130" x2="115" y2="150" stroke="#00F0FF" stroke-width="2"/>
  <circle cx="115" cy="150" r="3" fill="#00F0FF"/>

  <circle cx="427" cy="130" r="5" fill="#FF007F"/>
  <line x1="427" y1="130" x2="397" y2="150" stroke="#FF007F" stroke-width="2"/>
  <circle cx="397" cy="150" r="3" fill="#FF007F"/>

  <!-- Điểm nhấn năng lượng dưới đáy khiên -->
  <polygon points="256,430 270,448 256,466 242,448" fill="#00F0FF" filter="url(#neonGlow)"/>

  <!-- Dòng chữ NEON PARKING tinh tế dưới đế khiên -->
  <text x="256" y="415" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="22" 
        fill="#FFFFFF" letter-spacing="6" text-anchor="middle">NEON PARKING</text>
</svg>
'''

svg_path = os.path.join(OUTPUT_DIR, "logo.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"[OK] Đã tạo file SVG: {svg_path}")

# 2. Tạo hình ảnh PNG bằng Pillow (chất lượng sắc nét, trong suốt)
def tao_logo_pillow(kich_thuoc=512):
    # Vẽ ở độ phân giải gấp đôi (supersampling) để khử răng cưa
    scale = 2
    size = kich_thuoc * scale
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Hệ tọa độ tỉ lệ
    def s(val):
        return int(val * (size / 512))

    # Tọa độ khiên ngoài
    pts_shield = [
        (s(256), s(28)),
        (s(460), s(110)),
        (s(460), s(350)),
        (s(256), s(484)),
        (s(52), s(350)),
        (s(52), s(110))
    ]
    # Nền khiên
    draw.polygon(pts_shield, fill=(21, 25, 40, 235))

    # Viền khiên dày màu Cyan / Purple / Pink
    draw.polygon(pts_shield, outline=(0, 240, 255, 255), width=s(7))

    # Viền trong mờ
    pts_shield_inner = [
        (s(256), s(48)),
        (s(436), s(122)),
        (s(436), s(336)),
        (s(256), s(456)),
        (s(76), s(336)),
        (s(76), s(122))
    ]
    draw.polygon(pts_shield_inner, outline=(121, 40, 202, 160), width=s(3))

    # Thân xe thể thao Cyberpunk
    pts_windshield = [
        (s(256), s(165)),
        (s(330), s(235)),
        (s(182), s(235))
    ]
    draw.polygon(pts_windshield, fill=(0, 240, 255, 60), outline=(0, 240, 255, 200), width=s(3))

    pts_car = [
        (s(182), s(235)),
        (s(330), s(235)),
        (s(390), s(285)),
        (s(368), s(345)),
        (s(144), s(345)),
        (s(122), s(285))
    ]
    draw.polygon(pts_car, fill=(26, 31, 53, 255), outline=(255, 0, 127, 240), width=s(4))

    # Đèn pha xe Cyberpunk Cyan
    pts_headlight_l = [(s(138), s(295)), (s(175), s(295)), (s(192), s(305)), (s(130), s(305))]
    pts_headlight_r = [(s(374), s(295)), (s(337), s(295)), (s(320), s(305)), (s(382), s(305))]
    draw.polygon(pts_headlight_l, fill=(0, 240, 255, 255))
    draw.polygon(pts_headlight_r, fill=(0, 240, 255, 255))

    # Đèn gầm xe Pink Neon
    draw.line([(s(146), s(355)), (s(366), s(355))], fill=(255, 0, 127, 255), width=s(5))

    # Lưới tản nhiệt trung tâm xe
    pts_grill = [(s(222), s(312)), (s(290), s(312)), (s(280), s(332)), (s(232), s(332))]
    draw.polygon(pts_grill, fill=(13, 15, 24, 255), outline=(0, 240, 255, 180), width=s(2))

    # Chữ "P" PARKING TỎA SÁNG
    # Cột đứng của chữ P
    draw.rounded_rectangle(
        [s(225), s(85), s(245), s(205)],
        radius=s(4),
        fill=(0, 240, 255, 255)
    )
    # Vòng cong của chữ P
    draw.arc(
        [s(225), s(85), s(305), s(155)],
        start=270,
        end=90,
        fill=(255, 0, 127, 255),
        width=s(18)
    )
    draw.line([(s(235), s(94)), (s(265), s(94))], fill=(255, 0, 127, 255), width=s(18))
    draw.line([(s(235), s(146)), (s(265), s(146))], fill=(255, 0, 127, 255), width=s(18))

    # Chi tiết mạch điện tử 2 bên khiên
    draw.ellipse([s(82), s(128), s(92), s(138)], fill=(0, 240, 255, 255))
    draw.line([(s(87), s(133)), (s(115), s(155))], fill=(0, 240, 255, 200), width=s(3))
    draw.ellipse([s(110), s(150), s(120), s(160)], fill=(0, 240, 255, 255))

    draw.ellipse([s(420), s(128), s(430), s(138)], fill=(255, 0, 127, 255))
    draw.line([(s(425), s(133)), (s(397), s(155))], fill=(255, 0, 127, 200), width=s(3))
    draw.ellipse([s(392), s(150), s(402), s(160)], fill=(255, 0, 127, 255))

    # Biểu tượng năng lượng nhọn đáy khiên
    pts_bottom = [(s(256), s(425)), (s(272), s(445)), (s(256), s(465)), (s(240), s(445))]
    draw.polygon(pts_bottom, fill=(0, 240, 255, 255))

    # Thu nhỏ về đúng kích thước yêu cầu (Antialiasing Lanczos)
    img_resized = img.resize((kich_thuoc, kich_thuoc), Image.Resampling.LANCZOS)
    return img_resized

# 3. Xuất logo.png 512x512
img_512 = tao_logo_pillow(512)
png_512_path = os.path.join(OUTPUT_DIR, "logo.png")
img_512.save(png_512_path, "PNG")
print(f"[OK] Đã tạo file PNG 512x512: {png_512_path}")

# 4. Xuất logo_small.png 64x64
img_64 = tao_logo_pillow(64)
png_64_path = os.path.join(OUTPUT_DIR, "logo_small.png")
img_64.save(png_64_path, "PNG")
print(f"[OK] Đã tạo file PNG 64x64: {png_64_path}")

# 5. Xuất app.ico chứa đầy đủ các kích cỡ chuẩn Windows: 16, 24, 32, 48, 64, 128, 256
ico_path = os.path.join(OUTPUT_DIR, "app.ico")
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img_512.save(ico_path, format="ICO", sizes=ico_sizes)
print(f"[OK] Đã tạo file ICO đa kích cỡ: {ico_path}")
print("=== HOÀN TẤT BỘ BRANDING CYBERPUNK THÀNH CÔNG ===")
