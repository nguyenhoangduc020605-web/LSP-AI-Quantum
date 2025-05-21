
# Import các thư viện cần thiết
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Sửa lỗi UnicodeEncodeError trên Windows
import math
from scapy.all import Ether, IP, TCP, Raw, sendp

# Phần 1: Tạo cặp khóa RSA 8-bit (triển khai thủ công)
def tao_cap_khoa_8bit():
    p = 11  # Số nguyên tố 1
    q = 13  # Số nguyên tố 2
    n = p * q  # Modulus (n = p * q) = 143
    phi = (p - 1) * (q - 1)  # Hàm Euler's totient
    e = 7  # Public exponent
    d = pow(e, -1, phi)  # Private exponent
    return (n, d), (n, e)  # Trả về khóa riêng, khóa công khai

# Phần 2: Chuyển đổi khóa công khai thành chuỗi PEM (giả lập)
def khoa_cong_khai_sang_pem(khoa_cong_khai):
    n, e = khoa_cong_khai
    pem_data = f"-----BEGIN PUBLIC KEY-----\n" \
               f"n={n},e={e}\n" \
               f"-----END PUBLIC KEY-----"
    return pem_data

# Phần 3: Mã hóa RSA
def ma_hoa_rsa(van_ban, khoa_cong_khai):
    n, e = khoa_cong_khai
    # Chuyển văn bản thành số (ASCII) và mã hóa từng ký tự
    van_ban_ma_hoa = []
    for char in van_ban:
        m = ord(char)  # Chuyển ký tự thành ASCII
        c = pow(m, e, n)  # Mã hóa: c = m^e mod n
        van_ban_ma_hoa.append(str(c))  # Lưu dưới dạng chuỗi
    return ','.join(van_ban_ma_hoa)  # Trả về chuỗi các số cách nhau bởi dấu phẩy

# Phần 4: Người gửi
def nguoi_gui():
    print("Người gửi: Đang tạo cặp khóa RSA 8-bit...")
    khoa_rieng, khoa_cong_khai = tao_cap_khoa_8bit()
    print(f"Khóa công khai: {khoa_cong_khai}")
    print(f"Khóa riêng: {khoa_rieng}")

    print("\nNgười gửi: Đang chuyển đổi khóa công khai thành chuỗi PEM...")
    chuoi_pem = khoa_cong_khai_sang_pem(khoa_cong_khai)
    print("Chuỗi PEM:")
    print(chuoi_pem)

    print("\nNgười gửi: Đang mã hóa văn bản 'Hello World'...")
    van_ban = "Hello World"
    van_ban_ma_hoa = ma_hoa_rsa(van_ban, khoa_cong_khai)
    print(f"Văn bản mã hóa: {van_ban_ma_hoa}")

    print("\nNgười gửi: Đang gửi chuỗi PEM và văn bản mã hóa qua mạng...")
    # Tạo gói tin với Scapy
    packet = Ether() / IP(dst="127.0.0.1") / TCP(dport=1234) / Raw(load=f"{chuoi_pem}||{van_ban_ma_hoa}")
    sendp(packet, verbose=False)  # Sử dụng giao diện mặc định
    print("Người gửi: Đã gửi gói tin.")

if __name__ == "__main__":
    nguoi_gui()
