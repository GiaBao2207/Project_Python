"""
Script thiết kế bộ nhận diện logo trừu tượng cao cấp (Đợt 1 - Branding)
Tạo 3 phương án vector SVG và hình ảnh preview so sánh trên nền sáng & tối:
1. Option 1: Abstract Automotive (Khí động học & Làn đỗ phân tầng)
2. Option 2: Geometric Motion (Dòng chảy chuyển động & Cổng phân luồng)
3. Option 3: Negative Space Monogram (Chữ 'N' lồng ghép Làn xe & Ô đỗ)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPTIONS_DIR = os.path.join(BASE_DIR, "assets", "branding", "options")
BRANDING_DIR = os.path.join(BASE_DIR, "assets", "branding")
os.makedirs(OPTIONS_DIR, exist_ok=True)

# Bảng màu chuẩn Cyberpunk Premium
C_BG_DARK = "#0A0F14"
C_BG_LIGHT = "#F5F7FA"
C_SURFACE_DARK = "#131D25"
C_SURFACE_LIGHT = "#FFFFFF"
C_CARD_DARK = "#1E2A36"
C_CARD_LIGHT = "#E9EFF5"
C_BORDER_DARK = "#344552"
C_BORDER_LIGHT = "#CBD5E1"

C_TEAL = "#008C91"
C_TEAL_DARK = "#006B70"
C_TEAL_HOVER = "#08777D"
C_TEAL_LIGHT = "#00B4BC"
C_GOLD = "#C5A46D"
C_GOLD_LIGHT = "#E0C392"
C_WHITE = "#FFFFFF"
C_TEXT_DARK = "#F5F7FA"
C_TEXT_LIGHT = "#0A0F14"
C_MUTED_DARK = "#AEBAC5"
C_MUTED_LIGHT = "#64748B"

# ──────────────────────────────────────────────────────────────────────────
# 1. TẠO CÁC FILE SVG VECTOR NGUYÊN BẢN (CHÍNH XÁC & CHỈNH SỬA ĐƯỢC)
# ──────────────────────────────────────────────────────────────────────────

# Option 1 SVG: Abstract Automotive
svg_opt1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="tealGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00B4BC"/>
      <stop offset="100%" stop-color="#006B70"/>
    </linearGradient>
    <linearGradient id="goldGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E0C392"/>
      <stop offset="100%" stop-color="#C5A46D"/>
    </linearGradient>
  </defs>
  <!-- Blade 1: Mui xe & Khí động học nóc (Roofline) -->
  <polygon points="140,165 330,165 410,235 365,250 305,200 155,200" fill="url(#tealGrad1)"/>
  
  <!-- Blade 2: Thân xe & Vạch phân làn chính (Mid Contour & Main Bay) -->
  <polygon points="100,250 355,250 425,310 380,325 330,285 120,285" fill="#008C91"/>
  
  <!-- Blade 3: Chân đế sàn đỗ & Làn dẫn đường (Ground Guidance Slot) -->
  <polygon points="140,335 320,335 365,380 325,390 295,365 160,365" fill="#006B70"/>
  
  <!-- Accent Mũi xe mạ Champagne Gold (Aero Nose Cut) -->
  <polygon points="365,250 410,235 425,310 380,285" fill="url(#goldGrad1)"/>
  
  <!-- Điểm laser định vị thông minh (Smart Docking Laser Point) -->
  <polygon points="440,270 455,285 440,300 425,285" fill="#E0C392"/>
</svg>'''

# Option 2 SVG: Geometric Motion
svg_opt2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="tealGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00B4BC"/>
      <stop offset="100%" stop-color="#006B70"/>
    </linearGradient>
    <linearGradient id="goldGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E0C392"/>
      <stop offset="100%" stop-color="#C5A46D"/>
    </linearGradient>
  </defs>
  <!-- Vành chuyển động đa giác phía trên (Upper Flow Chevron) -->
  <polygon points="256,90 410,180 410,265 360,235 360,200 256,140 185,180 185,135" fill="url(#tealGrad2)"/>
  
  <!-- Vành chuyển động đối xứng phía dưới (Lower Flow Chevron) -->
  <polygon points="256,422 102,332 102,247 152,277 152,312 256,372 327,332 327,377" fill="#008C91"/>
  
  <!-- Khối ô đỗ xe trung tâm Negative Space & Prism (Central Vehicle Dock) -->
  <polygon points="256,180 330,256 256,332 182,256" fill="#131D25" stroke="#344552" stroke-width="4"/>
  
  <!-- Lõi điều phối mạ vàng Champagne Gold (Core Navigation Vector) -->
  <polygon points="256,195 305,245 256,295 207,245" fill="url(#goldGrad2)"/>
  
  <!-- Vệt định hướng xe vào bãi (Entry Slot) -->
  <polygon points="256,230 275,256 256,282 237,256" fill="#0A0F14"/>
</svg>'''

# Option 3 SVG: Negative Space Monogram
svg_opt3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="tealGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00B4BC"/>
      <stop offset="100%" stop-color="#008C91"/>
    </linearGradient>
    <linearGradient id="goldGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E0C392"/>
      <stop offset="100%" stop-color="#C5A46D"/>
    </linearGradient>
  </defs>
  <!-- Trụ trái chữ N (Left Strut - Vạch phân ranh giới đỗ) -->
  <polygon points="120,120 185,120 135,392 70,392" fill="#006B70"/>
  
  <!-- Trụ phải chữ N (Right Strut) -->
  <polygon points="377,120 442,120 392,392 327,392" fill="url(#tealGrad3)"/>
  
  <!-- Dải chéo khí động học liên kết chữ N (Dynamic Aero Blade) -->
  <polygon points="185,120 392,345 327,392 120,167" fill="#008C91"/>
  
  <!-- Vạch cắt góc mạ Champagne Gold (Negative Space Slot Divider) -->
  <polygon points="215,190 325,305 295,335 185,220" fill="url(#goldGrad3)"/>
  
  <!-- Vệt phản xạ ánh sáng công nghiệp mỏng -->
  <polygon points="120,120 185,120 175,135 110,135" fill="#E0C392"/>
</svg>'''

with open(os.path.join(OPTIONS_DIR, "option_1_abstract_automotive.svg"), "w", encoding="utf-8") as f:
    f.write(svg_opt1)
with open(os.path.join(OPTIONS_DIR, "option_2_geometric_motion.svg"), "w", encoding="utf-8") as f:
    f.write(svg_opt2)
with open(os.path.join(OPTIONS_DIR, "option_3_negative_space_monogram.svg"), "w", encoding="utf-8") as f:
    f.write(svg_opt3)

print("[OK] Đã xuất 3 file vector SVG nguyên bản chuẩn xác.")

# ──────────────────────────────────────────────────────────────────────────
# 2. HÀM VẼ CÁC OPTION BẰNG PIL SUPERSAMPLING (CHỐNG RĂNG CƯA TUYỆT ĐỐI)
# ──────────────────────────────────────────────────────────────────────────

SCALE = 4  # Vẽ ở 2048x2048 rồi downsample về 512x512

def draw_option_1(draw, offset_x=0, offset_y=0, scale=1.0, monochrome=None):
    """Vẽ Option 1: Abstract Automotive."""
    c_teal_hi = monochrome or C_TEAL_LIGHT
    c_teal_mid = monochrome or C_TEAL
    c_teal_lo = monochrome or C_TEAL_DARK
    c_gold = monochrome or C_GOLD
    c_gold_hi = monochrome or C_GOLD_LIGHT

    def tr(pts):
        return [(offset_x + x * scale, offset_y + y * scale) for x, y in pts]

    # Blade 1 (Roofline)
    draw.polygon(tr([(140, 165), (330, 165), (410, 235), (365, 250), (305, 200), (155, 200)]), fill=c_teal_hi)
    # Blade 2 (Mid Body)
    draw.polygon(tr([(100, 250), (355, 250), (425, 310), (380, 325), (330, 285), (120, 285)]), fill=c_teal_mid)
    # Blade 3 (Ground)
    draw.polygon(tr([(140, 335), (320, 335), (365, 380), (325, 390), (295, 365), (160, 365)]), fill=c_teal_lo)
    # Accent Gold Nose
    draw.polygon(tr([(365, 250), (410, 235), (425, 310), (380, 285)]), fill=c_gold)
    # Laser Point
    draw.polygon(tr([(440, 270), (455, 285), (440, 300), (425, 285)]), fill=c_gold_hi)

def draw_option_2(draw, offset_x=0, offset_y=0, scale=1.0, monochrome=None):
    """Vẽ Option 2: Geometric Motion."""
    c_teal_hi = monochrome or C_TEAL_LIGHT
    c_teal_mid = monochrome or C_TEAL
    c_gold = monochrome or C_GOLD
    c_inner_bg = "#131D25" if monochrome is None else monochrome
    c_inner_stroke = "#344552" if monochrome is None else monochrome

    def tr(pts):
        return [(offset_x + x * scale, offset_y + y * scale) for x, y in pts]

    # Upper Chevron
    draw.polygon(tr([(256, 90), (410, 180), (410, 265), (360, 235), (360, 200), (256, 140), (185, 180), (185, 135)]), fill=c_teal_hi)
    # Lower Chevron
    draw.polygon(tr([(256, 422), (102, 332), (102, 247), (152, 277), (152, 312), (256, 372), (327, 332), (327, 377)]), fill=c_teal_mid)
    
    if monochrome is None:
        # Central negative bay
        draw.polygon(tr([(256, 180), (330, 256), (256, 332), (182, 256)]), fill=c_inner_bg, outline=c_inner_stroke, width=int(3 * scale))
        # Gold Core
        draw.polygon(tr([(256, 195), (305, 245), (256, 295), (207, 245)]), fill=c_gold)
        # Inner slot cut
        draw.polygon(tr([(256, 230), (275, 256), (256, 282), (237, 256)]), fill=C_BG_DARK)
    else:
        # Monochrome core
        draw.polygon(tr([(256, 195), (305, 245), (256, 295), (207, 245)]), fill=monochrome)

def draw_option_3(draw, offset_x=0, offset_y=0, scale=1.0, monochrome=None):
    """Vẽ Option 3: Negative Space Monogram."""
    c_teal_lo = monochrome or C_TEAL_DARK
    c_teal_mid = monochrome or C_TEAL
    c_teal_hi = monochrome or C_TEAL_LIGHT
    c_gold = monochrome or C_GOLD
    c_gold_hi = monochrome or C_GOLD_LIGHT

    def tr(pts):
        return [(offset_x + x * scale, offset_y + y * scale) for x, y in pts]

    # Left Strut
    draw.polygon(tr([(120, 120), (185, 120), (135, 392), (70, 392)]), fill=c_teal_lo)
    # Right Strut
    draw.polygon(tr([(377, 120), (442, 120), (392, 392), (327, 392)]), fill=c_teal_hi)
    # Aero Blade Diagonal
    draw.polygon(tr([(185, 120), (392, 345), (327, 392), (120, 167)]), fill=c_teal_mid)
    # Gold Slot Cut
    draw.polygon(tr([(215, 190), (325, 305), (295, 335), (185, 220)]), fill=c_gold)
    # Light reflex
    draw.polygon(tr([(120, 120), (185, 120), (175, 135), (110, 135)]), fill=c_gold_hi)


def render_hi_res_logo(draw_func, size=512, monochrome=None):
    """Render logo với độ phân giải siêu nét (supersampling 4x)."""
    large_size = size * SCALE
    im = Image.new("RGBA", (large_size, large_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw_func(d, offset_x=0, offset_y=0, scale=(large_size / 512.0), monochrome=monochrome)
    return im.resize((size, size), Image.Resampling.LANCZOS)


# Xuất từng file PNG độc lập 512x512 nền trong suốt
for idx, fn in enumerate([draw_option_1, draw_option_2, draw_option_3], 1):
    logo_img = render_hi_res_logo(fn, size=512)
    logo_img.save(os.path.join(OPTIONS_DIR, f"option_{idx}.png"))
print("[OK] Đã xuất 3 file PNG 512x512 nền trong suốt cho 3 options.")


# ──────────────────────────────────────────────────────────────────────────
# 3. TẠO BẢN PREVIEW SO SÁNH TRỰC QUAN (DARK & LIGHT BOARDS)
# ──────────────────────────────────────────────────────────────────────────

def create_comparison_board(bg_color, text_color, card_bg, border_color, is_dark=True):
    """Tạo bảng so sánh đầy đủ 3 phương án trên nền sáng hoặc tối."""
    W = 1600
    H = 1100
    canvas = Image.new("RGBA", (W, H), bg_color)
    d = ImageDraw.Draw(canvas)

    # Thử nạp font hệ thống Windows Segoe UI
    try:
        font_hero = ImageFont.truetype("segoeuib.ttf", 34)
        font_sub = ImageFont.truetype("segoeui.ttf", 16)
        font_title = ImageFont.truetype("segoeuib.ttf", 22)
        font_tag = ImageFont.truetype("segoeuib.ttf", 13)
        font_desc = ImageFont.truetype("segoeui.ttf", 14)
        font_brand = ImageFont.truetype("segoeuib.ttf", 18)
        font_brand_sub = ImageFont.truetype("segoeui.ttf", 11)
        font_size_lbl = ImageFont.truetype("segoeui.ttf", 11)
    except Exception:
        font_hero = font_sub = font_title = font_tag = font_desc = font_brand = font_brand_sub = font_size_lbl = ImageFont.load_default()

    # Header
    d.text((60, 40), "NEON PARKING MANAGER — ĐỀ XUẤT NHẬN DIỆN THƯƠNG HIỆU", fill=text_color, font=font_hero)
    mode_text = "DARK MODE PREVIEW (#0A0F14)" if is_dark else "LIGHT MODE PREVIEW (#F5F7FA)"
    d.text((60, 85), f"PHONG CÁCH: ABSTRACT AUTOMOTIVE × CYBERPUNK PREMIUM × INDUSTRIAL LUXURY  |  {mode_text}", fill=C_TEAL if is_dark else C_TEAL_DARK, font=font_sub)

    # Đường phân cách header
    d.line([(60, 115), (W - 60, 115)], fill=border_color, width=1)

    cards_data = [
        {
            "num": "PHƯƠNG ÁN 01",
            "name": "ABSTRACT AUTOMOTIVE",
            "concept": "Khí Động Học & Làn Đỗ Phân Tầng",
            "desc": "Tạo hình từ 3 dải vuốt khí động học (aerodynamic blades) của mui xe thể thao lồng vào các vạch đỗ nghiêng. Mũi xe mạ Champagne Gold dứt khoát, hiện đại.",
            "draw": draw_option_1,
            "badge": "KHÍ ĐỘNG HỌC & TỐC ĐỘ"
        },
        {
            "num": "PHƯƠNG ÁN 02",
            "name": "GEOMETRIC MOTION",
            "concept": "Dòng Chảy & Cổng Phân Luồng",
            "desc": "Hai vành đa giác đan cài đối xứng tạo nên vòng tuần hoàn phương tiện. Khoảng trống trung tâm hình thoi định vị vị trí đỗ thông minh chuẩn xác.",
            "draw": draw_option_2,
            "badge": "TUẦN HOÀN & CÔNG NGHỆ"
        },
        {
            "num": "PHƯƠNG ÁN 03",
            "name": "NEGATIVE SPACE MONOGRAM",
            "concept": "Chữ 'N' Lồng Ghép Làn Xe & Ô Đỗ",
            "desc": "Monogram chữ N biểu trưng cho NEON. Hai khoảng âm bản (negative space) tạo hình đối xứng của hai ô đỗ xe ngầm. Nhận diện cực cao ở mọi kích thước.",
            "draw": draw_option_3,
            "badge": "ĐỀ XUẤT TỐI ƯU NHẤT ★"
        }
    ]

    card_w = 460
    card_h = 920
    spacing = 40
    start_x = 60
    start_y = 140

    for i, data in enumerate(cards_data):
        cx = start_x + i * (card_w + spacing)
        cy = start_y

        # Card container
        d.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=14, fill=card_bg, outline=C_GOLD if i == 2 else border_color, width=2 if i == 2 else 1)

        # Card header badge
        badge_color = C_GOLD if i == 2 else C_TEAL
        d.text((cx + 25, cy + 22), data["num"], fill=badge_color, font=font_tag)
        d.text((cx + 25, cy + 42), data["name"], fill=text_color, font=font_title)
        d.text((cx + 25, cy + 72), data["concept"], fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_sub)

        # Đường kẻ chia phần
        d.line([(cx + 25, cy + 100), (cx + card_w - 25, cy + 100)], fill=border_color, width=1)

        # 1. Main Icon Preview (180x180)
        icon_box_size = 190
        ib_x = cx + (card_w - icon_box_size) // 2
        ib_y = cy + 115
        d.rounded_rectangle([(ib_x, ib_y), (ib_x + icon_box_size, ib_y + icon_box_size)], radius=10, fill=C_BG_DARK if is_dark else "#F1F5F9", outline=border_color, width=1)

        main_icon = render_hi_res_logo(data["draw"], size=160)
        canvas.paste(main_icon, (ib_x + 15, ib_y + 15), main_icon)

        # 2. Typography Lockup (Horizontal Layout)
        lockup_y = cy + 325
        d.rounded_rectangle([(cx + 25, lockup_y), (cx + card_w - 25, lockup_y + 70)], radius=8, fill=C_BG_DARK if is_dark else "#F1F5F9", outline=border_color, width=1)
        small_icon = render_hi_res_logo(data["draw"], size=48)
        canvas.paste(small_icon, (cx + 40, lockup_y + 11), small_icon)
        d.text((cx + 102, lockup_y + 14), "NEON PARKING", fill=text_color, font=font_brand)
        d.text((cx + 104, lockup_y + 38), "MANAGER • SMART DESKTOP", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_brand_sub)

        # 3. Kích thước thực tế (Scalability: 64px, 32px, 24px)
        scale_box_y = cy + 415
        d.text((cx + 25, scale_box_y), "KHẢ NĂNG HIỂN THỊ KÍCH THƯỚC NHỎ:", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_tag)

        # 64px
        icon_64 = render_hi_res_logo(data["draw"], size=64)
        canvas.paste(icon_64, (cx + 35, scale_box_y + 25), icon_64)
        d.text((cx + 48, scale_box_y + 95), "64px", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_size_lbl)

        # 32px
        icon_32 = render_hi_res_logo(data["draw"], size=32)
        canvas.paste(icon_32, (cx + 145, scale_box_y + 40), icon_32)
        d.text((cx + 148, scale_box_y + 95), "32px", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_size_lbl)

        # 24px
        icon_24 = render_hi_res_logo(data["draw"], size=24)
        canvas.paste(icon_24, (cx + 225, scale_box_y + 44), icon_24)
        d.text((cx + 225, scale_box_y + 95), "24px", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_size_lbl)

        # Monochrome 32px
        mono_color = C_WHITE if is_dark else C_TEXT_LIGHT
        icon_mono = render_hi_res_logo(data["draw"], size=32, monochrome=mono_color)
        canvas.paste(icon_mono, (cx + 310, scale_box_y + 40), icon_mono)
        d.text((cx + 300, scale_box_y + 95), "1-MÀU (32px)", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_size_lbl)

        # Đường kẻ chia phần
        d.line([(cx + 25, cy + 545), (cx + card_w - 25, cy + 545)], fill=border_color, width=1)

        # 4. Mô tả ý tưởng & phân tích
        desc_y = cy + 560
        d.text((cx + 25, desc_y), "Ý TƯỞNG THIẾT KẾ:", fill=C_GOLD if i == 2 else C_TEAL, font=font_tag)

        # Wrap text mô tả
        words = data["desc"].split(" ")
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) > 42:
                lines.append(cur)
                cur = w
            else:
                cur = cur + " " + w if cur else w
        if cur:
            lines.append(cur)

        for l_idx, line in enumerate(lines):
            d.text((cx + 25, desc_y + 26 + l_idx * 22), line, fill=text_color, font=font_desc)

        # Đánh giá ưu điểm
        pros_y = desc_y + 160
        d.text((cx + 25, pros_y), "ƯU ĐIỂM NỔI BẬT:", fill=C_MUTED_DARK if is_dark else C_MUTED_LIGHT, font=font_tag)
        if i == 0:
            pros = ["• Đậm chất siêu xe & công nghệ tốc độ", "• Tỷ lệ vàng khí động học bất đối xứng", "• Nhận diện phong cách công nghiệp cơ khí"]
        elif i == 1:
            pros = ["• Tính tuần hoàn luân chuyển khép kín", "• Biểu tượng hiện đại, tối giản, cân xứng", "• Nhấn mạnh tính tổ chức thông minh của bãi xe"]
        else:
            pros = ["• Monogram chữ N độc quyền, dễ đăng ký bản quyền", "• Tận dụng Negative Space thông minh", "• Độ nhận diện tối đa khi thu nhỏ về 24px và app.ico"]

        for p_idx, pro in enumerate(pros):
            d.text((cx + 25, pros_y + 24 + p_idx * 22), pro, fill=C_GOLD if i == 2 else (C_TEAL_LIGHT if is_dark else C_TEAL_DARK), font=font_desc)

        # Badge đề xuất dưới chân
        footer_badge_y = cy + card_h - 55
        d.rounded_rectangle([(cx + 25, footer_badge_y), (cx + card_w - 25, footer_badge_y + 35)], radius=6, fill=C_GOLD if i == 2 else (C_TEAL_DARK if is_dark else C_CARD_LIGHT))
        badge_txt_color = "#0A0F14" if i == 2 else C_WHITE
        d.text((cx + 40, footer_badge_y + 8), data["badge"], fill=badge_txt_color, font=font_tag)

    return canvas


# Render và lưu bảng so sánh Dark và Light
board_dark = create_comparison_board(C_BG_DARK, C_TEXT_DARK, C_SURFACE_DARK, C_BORDER_DARK, is_dark=True)
board_dark.save(os.path.join(BRANDING_DIR, "preview_options_dark.png"))

board_light = create_comparison_board(C_BG_LIGHT, C_TEXT_LIGHT, C_SURFACE_LIGHT, C_BORDER_LIGHT, is_dark=False)
board_light.save(os.path.join(BRANDING_DIR, "preview_options_light.png"))

print("[OK] Đã tạo thành công 2 bảng preview so sánh chất lượng cao: preview_options_dark.png và preview_options_light.png.")
