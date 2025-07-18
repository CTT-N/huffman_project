"""Project: brief description about project
    To fulfil the requirement of FIT Course by Pham@PTIT
    Cao Thi Thanh Nhan - B23DCCN618
"""

# ===============================
# HÀM GHI / ĐỌC FILE NHỊ PHÂN
# ===============================

# Hàm ghi file nhị phân từ chuỗi bit đã mã hóa bằng Huffman.
def write_binary_file(path, bit_string):
    """
    Chuyển chuỗi bit (ví dụ: '011010...') thành dạng byte và ghi vào file nhị phân.
    Ghi kèm thông tin padding để khi đọc có thể khôi phục chính xác chuỗi ban đầu.
    """
    # Tính số bit padding cần thêm để độ dài bit_string chia hết cho 8
    padding = 8 - len(bit_string) % 8
    bit_string += '0' * padding  # Thêm padding vào cuối chuỗi bit
    # Ví dụ: '10101' → thêm 3 số 0 → '10101000'

    # Chuyển chuỗi bit thành mảng byte
    bytes_list = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]  # Cắt chuỗi thành từng nhóm 8 bit
        bytes_list.append(int(byte, 2))  # Chuyển từng nhóm thành số nguyên và thêm vào mảng

    # Ghi ra file nhị phân
    with open(path, 'wb') as f:
        f.write(bytes([padding]))     # Byte đầu tiên: ghi số bit padding
        f.write(bytes_list)           # Ghi toàn bộ dữ liệu nhị phân đã mã hóa


# Hàm đọc file nhị phân và phục hồi lại chuỗi bit ban đầu, dùng thông tin padding để cắt phần dư.
def read_binary_file(path):
    """
    Đọc file nhị phân được ghi bằng write_binary_file().
    Trả về chuỗi bit gốc sau khi loại bỏ phần padding.
    """
    with open(path, 'rb') as f:
        padding = int.from_bytes(f.read(1), 'big')  # Đọc byte đầu tiên: số padding
        byte_data = f.read()  # Đọc phần còn lại: dữ liệu nhị phân

        # Chuyển mỗi byte thành chuỗi nhị phân 8 bit và nối lại
        bit_string = ''.join(f'{byte:08b}' for byte in byte_data)

        # Loại bỏ số bit padding đã thêm ở cuối
        return bit_string[:-padding]

# ===============================
# VÍ DỤ MINH HỌA
# ===============================

# Giả sử bạn có chuỗi bit: '1010101'
# - Dài 7 bit → cần 1 bit padding → '10101010'
# - Ghi ra file:
#     + Byte đầu tiên: 1 (số padding)
#     + Byte thứ hai: 0b10101010 (170 ở hệ thập phân)
# - Khi đọc:
#     + Đọc byte đầu là 1 → biết cần bỏ 1 bit cuối → '10101010'[:-1] → '1010101'