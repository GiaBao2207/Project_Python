"""
NEON PARKING MANAGER - MODULE PLACEHOLDER VIEW
Khung giao diện placeholder hiển thị cho các module đang chờ phát triển ở các giai đoạn tiếp theo.
Hiển thị danh sách tính năng theo đúng Master Prompt và các thẻ KPI Cyberpunk mẫu.
"""

import customtkinter as ctk
from config.theme import CyberpunkTheme
from gui.components.stat_card import StatCard


# Cấu hình thông tin chi tiết từng phân hệ chuẩn hóa tên tiếng Việt
MODULE_INFO = {
    "dashboard": {
        "title": "Tổng quan bãi xe",
        "subtitle": "Theo dõi hoạt động và tình trạng bãi đỗ theo thời gian thực.",
        "icon": "⚡",
        "neon": CyberpunkTheme.PRIMARY_TEAL,
        "features": [
            "Giám sát tổng số xe đang gửi trong bãi (phân loại Xe máy, Ô tô, Xe đạp).",
            "Theo dõi sức chứa tối đa và số chỗ trống theo thời gian thực.",
            "Thống kê lượt xe vào / xe ra trong ngày.",
            "Báo cáo doanh thu hôm nay (chỉ hiển thị theo phân quyền).",
            "Bảng danh sách các phương tiện vừa vào/ra gần nhất."
        ],
        "kpis": [
            ("XE ĐANG GỬI", "—", "Thời gian thực", CyberpunkTheme.PRIMARY_TEAL, "⚡"),
            ("CHỖ TRỐNG HIỆN CÓ", "—", "Thời gian thực", CyberpunkTheme.SUCCESS, "🅿"),
            ("LƯỢT VÀO HÔM NAY", "—", "Thời gian thực", CyberpunkTheme.CHAMPAGNE_GOLD, "📥"),
            ("DOANH THU HÔM NAY", "—", "Thời gian thực", CyberpunkTheme.PRIMARY_TEAL, "💰")
        ]
    },
    "parking": {
        "title": "Quản lý bãi đỗ",
        "subtitle": "Giám sát sức chứa, chỗ trống và trạng thái tiếp nhận.",
        "icon": "🅿",
        "neon": CyberpunkTheme.PRIMARY_TEAL,
        "features": [
            "Theo dõi trực quan công suất và tỷ lệ lấp đầy các phân khu bãi xe.",
            "Giám sát số lượng chỗ trống riêng biệt cho Xe máy, Ô tô và Xe đạp.",
            "Cảnh báo tức thời khi bãi đạt ngưỡng đầy sức chứa.",
            "Tự động đồng bộ số liệu chỗ đỗ theo từng lượt xe ra vào."
        ],
        "kpis": [
            ("TỔNG SỨC CHỨA", "—", "Chỗ quy định", CyberpunkTheme.PRIMARY_TEAL, "🅿"),
            ("XE ĐANG ĐỖ", "—", "Thời gian thực", CyberpunkTheme.WARNING, "🚗"),
            ("CHỖ CÒN TRỐNG", "—", "Sẵn sàng tiếp nhận", CyberpunkTheme.SUCCESS, "✔")
        ]
    },
    "vehicles": {
        "title": "Quản lý phương tiện",
        "subtitle": "Tiếp nhận, theo dõi và xử lý phương tiện ra vào bãi.",
        "icon": "🚗",
        "neon": CyberpunkTheme.PRIMARY_TEAL,
        "features": [
            "Tiếp nhận phương tiện vào bãi, cấp mã vé tự động an toàn.",
            "Tra cứu phương tiện đang gửi với bộ lọc thông minh đa tiêu chí.",
            "Xử lý xe ra bãi, tự động tính toán thời gian và mức phí tương ứng.",
            "Ghi nhận phương thức thanh toán linh hoạt: Tiền mặt hoặc Chuyển khoản."
        ],
        "kpis": [
            ("XE MÁY", "—", "Đang gửi", CyberpunkTheme.PRIMARY_TEAL, "🛵"),
            ("Ô TÔ", "—", "Đang gửi", CyberpunkTheme.CHAMPAGNE_GOLD, "🚙"),
            ("XE ĐẠP", "—", "Đang gửi", CyberpunkTheme.SUCCESS, "🚲")
        ]
    },
    "tickets": {
        "title": "Quản lý vé xe",
        "subtitle": "Tra cứu vé, trạng thái gửi xe và lịch sử sử dụng.",
        "icon": "🎫",
        "neon": CyberpunkTheme.PRIMARY_TEAL,
        "features": [
            "Tra cứu nhanh vé xe theo mã vé, biển số, mã định danh hoặc chủ xe.",
            "Lọc trạng thái vé đa dạng: Đang gửi trong bãi hoặc Đã thanh toán.",
            "Xem chi tiết toàn diện thông tin vé, lịch sử vào/ra và snapshot bảng giá.",
            "Hỗ trợ thanh toán xe ra trực tiếp từ danh sách vé đang gửi."
        ],
        "kpis": [
            ("TỔNG SỐ VÉ", "—", "Toàn hệ thống", CyberpunkTheme.PRIMARY_TEAL, "🎫"),
            ("VÉ ĐANG GỬI", "—", "Trong bãi", CyberpunkTheme.WARNING, "⏳"),
            ("VÉ ĐÃ THANH TOÁN", "—", "Đã rời bãi", CyberpunkTheme.SUCCESS, "✔")
        ]
    },
    "revenue": {
        "title": "Quản lý doanh thu",
        "subtitle": "Theo dõi thanh toán, doanh thu và lịch sử giao dịch.",
        "icon": "💰",
        "neon": CyberpunkTheme.CHAMPAGNE_GOLD,
        "features": [
            "Tổng doanh thu toàn bãi, doanh thu hôm nay, doanh thu theo ngày và theo tháng.",
            "Phân tách phương thức thanh toán: Tiền mặt vs Chuyển khoản ngân hàng.",
            "Lịch sử chi tiết từng giao dịch thu tiền liên kết 1-1 với mã vé xe.",
            "Chỉ tính các giao dịch thanh toán thành công, loại trừ vé chưa trả tiền.",
            "Kiểm soát phân quyền chặt chẽ: Chỉ Quản trị viên (ADMIN) được truy cập."
        ],
        "kpis": [
            ("TỔNG DOANH THU", "—", "Đã thu", CyberpunkTheme.CHAMPAGNE_GOLD, "💎"),
            ("TIỀN MẶT", "—", "Tại quầy", CyberpunkTheme.SUCCESS, "💵"),
            ("CHUYỂN KHOẢN", "—", "Ngân hàng", CyberpunkTheme.PRIMARY_TEAL, "💳")
        ]
    },
    "statistics": {
        "title": "Thống kê hoạt động",
        "subtitle": "Phân tích lượt xe, loại phương tiện và mức sử dụng bãi.",
        "icon": "📊",
        "neon": CyberpunkTheme.SUCCESS,
        "features": [
            "Thống kê tổng lượng xe và phân bố tỷ trọng từng loại phương tiện.",
            "Biểu đồ số lượt phương tiện vào/ra theo ngày và theo tháng.",
            "Tỷ lệ lấp đầy và sử dụng sức chứa bãi xe.",
            "Phân tích giờ cao điểm tiếp nhận phương tiện trong ngày."
        ],
        "kpis": [
            ("TỶ LỆ LẤP ĐẦY", "—", "Bình quân", CyberpunkTheme.SUCCESS, "📈"),
            ("LƯỢT XE CAO ĐIỂM", "—", "Khung giờ vàng", CyberpunkTheme.PRIMARY_TEAL, "⏰"),
            ("TỶ TRỌNG LOẠI XE", "—", "Phân bố", CyberpunkTheme.CHAMPAGNE_GOLD, "🛵")
        ]
    },
    "users": {
        "title": "Quản lý nhân viên",
        "subtitle": "Quản lý tài khoản, trạng thái và quyền truy cập.",
        "icon": "👥",
        "neon": CyberpunkTheme.CHAMPAGNE_GOLD,
        "features": [
            "Danh sách toàn bộ nhân viên và tài khoản trong hệ thống.",
            "Admin tạo mới tài khoản nhân viên (băm mật khẩu bằng Argon2id).",
            "Khóa / Mở khóa tài khoản nhân viên tạm ngưng công tác.",
            "Đặt lại mật khẩu cho nhân viên qua quy trình an toàn.",
            "Chặn nhân viên tự nâng quyền Admin trái phép."
        ],
        "kpis": [
            ("QUẢN TRỊ VIÊN", "—", "Quản lý cấp cao", CyberpunkTheme.CHAMPAGNE_GOLD, "👑"),
            ("NHÂN VIÊN TRỰC", "—", "Vận hành ca trực", CyberpunkTheme.PRIMARY_TEAL, "👔"),
            ("TÀI KHOẢN KHÓA", "—", "Ngừng hoạt động", CyberpunkTheme.TEXT_MUTED, "🔒")
        ]
    },
    "settings": {
        "title": "Cấu hình hệ thống",
        "subtitle": "Thiết lập bảng giá, sức chứa và quy định vận hành.",
        "icon": "⚙️",
        "neon": CyberpunkTheme.PRIMARY_TEAL,
        "features": [
            "Price Settings: Xem và điều chỉnh bảng giá vé từng loại xe (Xe máy, Ô tô, Xe đạp).",
            "Nguyên tắc snapshot: Việc đổi giá mới không ảnh hưởng đến các vé đang gửi hoặc vé cũ.",
            "Capacity Settings: Cấu hình tổng số chỗ đỗ quy định cho từng phân khu.",
            "Quy tắc an toàn: Không cho phép giảm sức chứa xuống thấp hơn số xe đang gửi thực tế."
        ],
        "kpis": [
            ("GIÁ XE MÁY", "—", "VND / lượt", CyberpunkTheme.PRIMARY_TEAL, "🛵"),
            ("GIÁ Ô TÔ", "—", "VND / lượt", CyberpunkTheme.CHAMPAGNE_GOLD, "🚙"),
            ("GIÁ XE ĐẠP", "—", "VND / lượt", CyberpunkTheme.SUCCESS, "🚲")
        ]
    },
    "reports": {
        "title": "Xuất báo cáo",
        "subtitle": "Tổng hợp và xuất dữ liệu quản lý ra tệp TXT.",
        "icon": "📄",
        "neon": CyberpunkTheme.SUCCESS,
        "features": [
            "Xuất danh sách các phương tiện đang gửi ra file định dạng TXT chuyên nghiệp.",
            "Xuất lịch sử vé xe vào/ra theo khoảng ngày chọn lọc.",
            "Xuất bảng tổng hợp doanh thu theo ngày phục vụ bàn giao ca trực.",
            "Cho phép người dùng tùy chọn thư mục và tên file lưu trữ trên máy tính.",
            "Sử dụng chuẩn mã hóa UTF-8 bảo toàn tiếng Việt có dấu hoàn hảo."
        ],
        "kpis": [
            ("BÁO CÁO XE GỬI", "—", "Tệp văn bản", CyberpunkTheme.SUCCESS, "📄"),
            ("BÁO CÁO DOANH THU", "—", "Tệp văn bản", CyberpunkTheme.PRIMARY_TEAL, "📑"),
            ("LỊCH SỬ VÉ XE", "—", "Tệp văn bản", CyberpunkTheme.CHAMPAGNE_GOLD, "📋")
        ]
    },
    "audit": {
        "title": "Nhật ký hệ thống",
        "subtitle": "Theo dõi lịch sử thao tác và thay đổi quan trọng.",
        "icon": "🛡️",
        "neon": CyberpunkTheme.PRIMARY_TEAL,
        "features": [
            "Ghi nhận chi tiết mọi thao tác: Đăng nhập, Đăng xuất, Đổi mật khẩu.",
            "Lưu vết lịch sử tiếp nhận xe, xe ra, thu tiền, chỉnh sửa bảng giá, điều chỉnh sức chứa.",
            "Bảng tra cứu lịch sử dành riêng cho Quản trị viên phục vụ kiểm toán nội bộ.",
            "Dữ liệu được ghi nhận tự động vào bảng nhat_ky trong MySQL."
        ],
        "kpis": [
            ("SỰ KIỆN GHI NHẬN", "—", "Nhật ký kiểm toán", CyberpunkTheme.PRIMARY_TEAL, "🛡️"),
            ("ĐĂNG NHẬP GẦN NHẤT", "—", "Phiên làm việc", CyberpunkTheme.SUCCESS, "🕒"),
            ("CẢNH BÁO AN TOÀN", "—", "Tình trạng", CyberpunkTheme.CHAMPAGNE_GOLD, "✔")
        ]
    }
}


class PlaceholderView(ctk.CTkFrame):
    """
    View hiển thị thông tin giới thiệu và các thẻ KPI mẫu cho các module chưa làm.
    """
    def __init__(self, master, module_id: str, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)
        self.module_id = module_id
        info = MODULE_INFO.get(module_id, {
            "title": f"MODULE: {module_id.upper()}",
            "icon": "⚡",
            "neon": CyberpunkTheme.CYAN_NEON,
            "features": ["Module đang được hoàn thiện theo Master Prompt."],
            "kpis": []
        })

        # Vùng cuộn chính
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        # 1. Hàng thẻ KPI phía trên cùng
        if info.get("kpis"):
            kpi_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            kpi_frame.pack(fill="x", pady=(0, 20))

            for item in info["kpis"]:
                card = StatCard(
                    kpi_frame,
                    title=item[0],
                    value=item[1],
                    subtitle=item[2],
                    neon_color=item[3],
                    icon=item[4]
                )
                card.pack(side="left", fill="both", expand=True, padx=6)

        # 2. Khung Card lớn giới thiệu chi tiết module
        main_card = ctk.CTkFrame(
            scroll,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=info["neon"]
        )
        main_card.pack(fill="both", expand=True, pady=6)

        inner = ctk.CTkFrame(main_card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        # Badge trạng thái rõ ràng: Đang phát triển
        badge = ctk.CTkLabel(
            inner,
            text="⚡ CHỨC NĂNG ĐANG PHÁT TRIỂN",
            font=("Segoe UI", 9, "bold"),
            text_color=info["neon"],
            fg_color=CyberpunkTheme.SURFACE_CARD,
            corner_radius=6,
            padx=10,
            pady=4
        )
        badge.pack(anchor="w", pady=(0, 10))

        lbl_title = ctk.CTkLabel(
            inner,
            text=f"{info['icon']}  {info['title']}",
            font=CyberpunkTheme.FONT_TITLE_HERO,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            anchor="w"
        )
        lbl_title.pack(anchor="w", pady=(0, 8))

        lbl_desc = ctk.CTkLabel(
            inner,
            text="Nền tảng giao diện Cyberpunk, Hệ thống phân quyền AuthService và Cơ sở dữ liệu MySQL đã sẵn sàng.\nModule này sẽ được kích hoạt ngay sau khi hoàn tất kiểm tra nghiệm thu nền tảng.",
            font=CyberpunkTheme.FONT_SUBTITLE,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="left",
            anchor="w"
        )
        lbl_desc.pack(anchor="w", pady=(0, 18))

        # Phân cách
        ctk.CTkFrame(inner, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", pady=(0, 18))

        # Danh sách tính năng theo Master Prompt
        lbl_features_head = ctk.CTkLabel(
            inner,
            text="CÁC CHỨC NĂNG NGHIỆP VỤ ĐÃ ĐƯỢC THIẾT KẾ:",
            font=CyberpunkTheme.FONT_BODY_BOLD,
            text_color=info["neon"],
            anchor="w"
        )
        lbl_features_head.pack(anchor="w", pady=(0, 10))

        for feat in info["features"]:
            f_row = ctk.CTkFrame(inner, fg_color="transparent")
            f_row.pack(fill="x", pady=4)

            dot = ctk.CTkLabel(
                f_row,
                text="✔",
                font=("Segoe UI", 11, "bold"),
                text_color=info["neon"],
                width=24
            )
            dot.pack(side="left")

            txt = ctk.CTkLabel(
                f_row,
                text=feat,
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_PRIMARY,
                anchor="w"
            )
            txt.pack(side="left", fill="x", expand=True)
