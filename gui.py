"""Project: brief description about project
    To fulfil the requirement of FIT Course by Pham@PTIT
    Cao Thi Thanh Nhan - B23DCCN618
"""

# =============================================
# GIAO DIỆN NGƯỜI DÙNG CHO NÉN/GIẢI NÉN HUFFMAN
# =============================================

import tkinter as tk  # Dùng Tkinter để tạo giao diện GUI
from tkinter import filedialog, messagebox  # Hộp thoại chọn file và thông báo
from huffman import encode, decode, serialize_tree, deserialize_tree  # Thuật toán Huffman
from utils import write_binary_file, read_binary_file  # Xử lý đọc/ghi file nhị phân
import os  # Thao tác với file hệ thống

# =====================
# Hàm nén file người dùng chọn
# =====================
def select_file_to_encode():
    """Hiển thị hộp thoại chọn file để nén và lưu kết quả dưới dạng .huff."""
    filepath = filedialog.askopenfilename(title="Chọn file để nén")
    if not filepath:
        return  # Người dùng hủy chọn

    with open(filepath, 'rb') as f:
        data = f.read()  # Đọc nội dung file dưới dạng byte (chế độ nhị phân)

    encoded, tree = encode(data)  # Mã hóa dữ liệu bằng thuật toán Huffman
    tree_bits = serialize_tree(tree)  # Tuần tự hóa cây Huffman thành chuỗi bit

    separator = f'{ord("|"):08b}'  # Dùng '|' làm dấu phân cách (mã ASCII 124 → '01111100')
    bit_string = tree_bits + separator + encoded  # Ghép cây + phân cách + dữ liệu

    output_path = filedialog.asksaveasfilename(
        defaultextension=".huff",
        filetypes=[("Huffman Files", "*.huff")]
    )
    if output_path:
        write_binary_file(output_path, bit_string)  # Ghi chuỗi bit vào file nén
        ratio = (len(encoded) / (len(data) * 8)) * 100  # Tính tỷ lệ nén (%)
        messagebox.showinfo("Xong", f"Nén thành công!\nTỷ lệ nén: {ratio:.2f}%") # Hiển thị kết quả

# =====================
# Hàm giải nén file .huff
# =====================
def select_file_to_decode():
    """Hiển thị hộp thoại chọn file .huff để giải nén và lưu kết quả."""
    filepath = filedialog.askopenfilename(
        title="Chọn file .huff để giải nén",
        filetypes=[("Huffman Files", "*.huff")]
    )
    if not filepath:
        return  # Người dùng hủy chọn

    bit_string = read_binary_file(filepath)  # Đọc chuỗi bit từ file nén

    try:
        sep = f'{ord("|"):08b}'  # Dấu phân cách ('01111100')
        index = bit_string.index(sep)  # Tìm vị trí dấu phân cách

        tree_bits = bit_string[:index]  # Phần cây Huffman
        encoded_data = bit_string[index + 8:]  # Phần dữ liệu mã hóa

        tree = deserialize_tree(tree_bits)  # Khôi phục cây Huffman từ chuỗi bit
        decoded_bytes = decode(encoded_data, tree)  # Giải mã dữ liệu

        output_path = filedialog.asksaveasfilename(
            title="Lưu file giải nén",
            defaultextension=".out",
            filetypes=[("All Files", "*.*")]
        )
        if output_path: #Cho người dùng chọn nơi lưu file sau khi giải nén
            with open(output_path, 'wb') as f:
                f.write(decoded_bytes)
            messagebox.showinfo("Xong", "Giải nén thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Giải mã thất bại: {str(e)}")

# =====================
# Tạo giao diện chính
# =====================
root = tk.Tk()
root.title("Huffman Codec - Ứng dụng thực tế")

# Tiêu đề và nút chức năng
tk.Label(root, text="Huffman Codec cho Mọi File", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="🔐 Nén file bất kỳ", command=select_file_to_encode, width=30).pack(pady=10)
tk.Button(root, text="🔓 Giải nén file .huff", command=select_file_to_decode, width=30).pack(pady=10)

# Bắt đầu vòng lặp GUI
root.mainloop()

# =====================
# Ví dụ minh họa
# =====================
# Với chuỗi gốc "ly thuyet thong tin"
# B1_Tính độ dài gốc: giả sử mỗi kí tự dùng 1 byte = 8 bit, và chuỗi có 21 kí tự
#   -> 21 * 8 = 168 bit
# B2_Tính độ dài sau khi mã hóa Huffman
#   Sử dụng bảng mã Huffman xây dựng được ở mục Ví dụ minh hóa từ file huffman.py, ta có:
#   Tổng số bit sau khi mã hóa: 5 + 3 + 9 + 9 + 6 + 5 + 5 + 6 + 9 + 5 + 6 = 68 bit
# B3_Tính tỷ lệ nén
#   68 * 100% / 168 ≈ 40,48%