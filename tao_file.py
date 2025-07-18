"""Project: brief description about project
    To fulfil the requirement of FIT Course by Pham@PTIT
    Cao Thi Thanh Nhan - B23DCCN618
"""

# Tạo file mẫu để kiểm thử
### Bước 1: Tạo văn bản gốc
text = "ly thuyet thong tin"

### Bước 2: Mã hóa văn bản bằng Huffman
from huffman import encode, serialize_tree # encode() dùng để mã hóa, serialize_tree() dùng để tuần tự hóa cây Huffman
from utils import write_binary_file  # write_binary_file() dùng để ghi tệp nhị phân

encoded, tree = encode(text) # Thu được chuỗi nhị phân và cây Huffman tương ứng
tree_bin = serialize_tree(tree) # Chuyển cây Huffman thành chuỗi nhị phân để lưu trữ cùng với dữ liệu đã mã hóa

### Bước 3: Ghép cây và dữ liệu mã hóa vào một chuỗi nhị phân
separator = f'{ord("|"):08b}'  # Dùng ký tự '|' làm dấu phân cách giữa phần cây và phần dữ liệu đã mã hóa
bit_string = tree_bin + separator + encoded

### Bước 4: Ghi file gốc và file mã hóa
with open("lttt.txt", "w", encoding="utf-8") as f:
    f.write(text)

write_binary_file("lttt.bin", bit_string)

### Bước 5: Thông báo kết quả
print("File .txt đã tạo tại: lttt.txt")
print("File .bin đã tạo tại: lttt.bin")