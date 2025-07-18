"""Project: brief description about project
    To fulfil the requirement of FIT Course by Pham@PTIT
    Cao Thi Thanh Nhan - B23DCCN618
"""

# THUẬT TOÁN MÃ HÓA HUFFMAN TOÀN DIỆN

import heapq
from collections import Counter

# ===============================
# Lớp Node đại diện cho một nút trong cây Huffman.
# ===============================
class Node:
    def __init__(self, byte, freq):
        self.byte = byte      # Giá trị byte (0–255) hoặc None nếu là nút trong.
        self.freq = freq      # Tần suất xuất hiện của byte.
        self.left = None      # Con trái.
        self.right = None     # Con phải.

    def __lt__(self, other):
        """Hàm hỗ trợ so sánh trong heapq (ưu tiên tần suất nhỏ hơn)."""
        return self.freq < other.freq

# ===============================
# Hàm xây dựng cây Huffman từ dữ liệu đầu vào.
# ===============================
def build_tree(data):
    freq = Counter(data)  # Đếm tần suất xuất hiện của từng byte.
    heap = [Node(b, f) for b, f in freq.items()]  # Tạo các nút và đưa vào heap.
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)  # Gộp hai nút tần suất thấp nhất.
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]  # Trả về gốc cây.

# ===============================
# Hàm sinh bảng mã Huffman cho từng byte.
# ===============================
def generate_codes(node, prefix='', code_table=None):
    if code_table is None:
        code_table = {}
    if node.byte is not None:
        code_table[node.byte] = prefix  # Nút lá → ánh xạ byte sang chuỗi nhị phân.
    else:
        generate_codes(node.left, prefix + '0', code_table)
        generate_codes(node.right, prefix + '1', code_table)
    return code_table

# ===============================
# Hàm mã hóa dữ liệu đầu vào thành chuỗi bit.
# ===============================
def encode(data: bytes):
    tree = build_tree(data)
    code_table = generate_codes(tree)
    encoded = ''.join(code_table[b] for b in data)
    return encoded, tree  # Trả về chuỗi bit và cây Huffman để giải mã.

# ===============================
# Hàm giải mã chuỗi bit dựa trên cây Huffman.
# ===============================
def decode(encoded, tree):
    node = tree
    decoded = bytearray()
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.byte is not None:
            decoded.append(node.byte)
            node = tree  # Quay lại gốc để tiếp tục giải mã ký tự tiếp theo.
    return bytes(decoded)

# ===============================
# Hàm tuần tự hóa cây Huffman thành chuỗi bit.
# ===============================
def serialize_tree(node):
    if node.byte is not None:
        return '1' + f'{node.byte:08b}'  # Mã hóa nút lá: '1' + 8 bit giá trị byte.
    else:
        return '0' + serialize_tree(node.left) + serialize_tree(node.right)  # Nút trong: '0' + đệ quy trái + phải.

# ===============================
# Hàm giải tuần tự hóa để phục hồi cây Huffman từ chuỗi bit.
# ===============================
def deserialize_tree(bits):
    def helper(it):
        flag = next(it)
        if flag == '1':
            byte_str = ''.join(next(it) for _ in range(8))
            return Node(int(byte_str, 2), 0)
        else:
            left = helper(it)
            right = helper(it)
            node = Node(None, 0)
            node.left = left
            node.right = right
            return node
    return helper(iter(bits))

# ===============================
# Ví dụ minh họa
# ===============================
# Với đoạn thông tin: "ly thuyet thong tin ki", ta xây dựng được bảng mã Huffman như sau
# | Ký tự   | Số lần xuất hiện | Mã Huffman | Độ dài mã | Tổng số bit |
# | l       | 1                | 01100      | 5         | 5           |
# | y       | 1                | 111        | 3         | 3           |
# | (space) | 3                | 000        | 3         | 9           |
# | t       | 3                | 001        | 3         | 9           |
# | h       | 2                | 100        | 3         | 6           |
# | u       | 1                | 01101      | 5         | 5           |
# | e       | 1                | 01110      | 5         | 5           |
# | o       | 2                | 110        | 3         | 6           |
# | n       | 3                | 010        | 3         | 9           |
# | g       | 1                | 01111      | 5         | 5           |
# | i       | 2                | 101        | 3         | 6           |
# Chuỗi "ly thuyet thong tin" được mã hóa thành chuỗi bit:
# 01100 111 000 001 01101 111 01110 001 110 000 010 110 01111 000 010 101 001
