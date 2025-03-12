from datetime import datetime

def convert_to_iso_date(date_str):
    """
    Chuyển đổi định dạng ngày từ các chuỗi phổ biến về YYYY-MM-DD.
    
    Hỗ trợ các định dạng đầu vào phổ biến:
    - "Thu Mar 06 2025 07:00:00 GMT+0700 (Giờ Đông Dương)"
    - "2025-03-06T07:00:00Z"
    - "06/03/2025" hoặc "06-03-2025"
    
    Trả về:
    - Chuỗi ngày có định dạng YYYY-MM-DD nếu hợp lệ
    - None nếu lỗi
    """
    if not date_str:
        return None

    formats = [
        "%a %b %d %Y %H:%M:%S %Z%z",  # "Thu Mar 06 2025 07:00:00 GMT+0700"
        "%Y-%m-%dT%H:%M:%S%z",        # "2025-03-06T07:00:00Z"
        "%d/%m/%Y",                   # "06/03/2025"
        "%d-%m-%Y",                   # "06-03-2025"
        "%Y-%m-%d",                   # "2025-03-06"
    ]

    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%Y-%m-%d")  # Chuyển về YYYY-MM-DD
        except ValueError:
            continue  # Thử format tiếp theo nếu lỗi

    return None  # Nếu không có định dạng nào khớp