import sys
sys.stdout.reconfigure(encoding='utf-8')  # Sửa lỗi UnicodeEncodeError trên Windows
import math
import fractions
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt  # Thêm Matplotlib để vẽ biểu đồ

# Hàm vẽ biểu đồ xác suất
def ve_bieu_do_xac_suat(counts, counting_qubits, a, N):
    # Tính tổng số shots
    total_shots = sum(counts.values())
    
    # Chuẩn bị dữ liệu cho biểu đồ
    values = []
    probabilities = []
    for measured_str, count in counts.items():
        measured_value = int(measured_str, 2)
        probability = count / total_shots
        values.append(measured_value)
        probabilities.append(probability)
    
    # Vẽ histogram
    plt.figure(figsize=(10, 6))
    plt.bar(values, probabilities, width=2, align='center')
    plt.xlabel('Giá trị đo được (c)')
    plt.ylabel('Xác suất')
    plt.title(f'Xác suất các giá trị đo được với a = {a}, N = {N}')
    plt.grid(True)
    
    # Lưu biểu đồ
    plt.savefig(f'probability_a_{a}_N_{N}.png')
    plt.close()

def chay_thuat_toan_shor(N, max_attempts=10):
    # Thử nhiều giá trị a từ 2 đến max_attempts
    for a in range(2, min(max_attempts + 2, N)):
        print(f"Thử a = {a}...")
        # Kiểm tra GCD trước
        if math.gcd(a, N) != 1:
            factors = [math.gcd(a, N), N // math.gcd(a, N)]
            print(f"Tìm thấy thừa số bằng GCD: {factors}")
            return factors

        # Tạo mạch lượng tử
        n = int(np.ceil(np.log2(N)))
        counting_qubits = 2 * n
        target_qubits = n

        counting = QuantumRegister(counting_qubits, 'count')
        target = QuantumRegister(target_qubits, 'target')
        classical = ClassicalRegister(counting_qubits, 'meas')
        circuit = QuantumCircuit(counting, target, classical)

        # Áp dụng cổng Hadamard để tạo chồng chất
        circuit.h(counting)
        # Áp dụng cổng điều khiển đơn giản (giả lập phép tính mô-đun)
        for i in range(counting_qubits):
            circuit.cx(counting[i], target[0])

        # Đo thanh ghi đếm
        circuit.measure(counting, classical)

        # Chạy mô phỏng với số shots tăng
        backend = AerSimulator()
        job = backend.run(circuit, shots=1000)  # Tăng shots
        result = job.result()
        counts = result.get_counts()
        print(f"Counts cho a = {a}: {counts}")

        # Vẽ biểu đồ xác suất
        print(f"Vẽ biểu đồ xác suất cho a = {a}...")
        ve_bieu_do_xac_suat(counts, counting_qubits, a, N)

        # Tìm chu kỳ
        for measured_str, count in counts.items():
            measured_value = int(measured_str, 2)
            phase = measured_value / (2 ** counting_qubits)
            if phase == 0:
                continue
            frac = fractions.Fraction(phase).limit_denominator(N)
            r = frac.denominator
            print(f"Chu kỳ tiềm năng r = {r} cho measured_value = {measured_value}")
            if r % 2 == 0:
                x = pow(a, r // 2, N)
                factors = [math.gcd(x - 1, N), math.gcd(x + 1, N)]
                if factors[0] != 1 and factors[0] != N and factors[1] != 1 and factors[1] != N:
                    print(f"Tìm thấy thừa số với a = {a}, r = {r}: {factors}")
                    return factors
        print(f"Không tìm thấy thừa số với a = {a}")
    return None

# Các hàm khác giữ nguyên
def pem_sang_khoa_cong_khai(chuoi_pem):
    lines = chuoi_pem.split('\n')
    for line in lines:
        if line.startswith('n='):
            n, e = line.split(',')
            n = int(n.split('=')[1])
            e = int(e.split('=')[1])
            return (n, e)
    raise ValueError("Định dạng PEM không hợp lệ")

def giai_ma_rsa(van_ban_ma_hoa, khoa_rieng):
    n, d = khoa_rieng
    van_ban_ma_hoa = van_ban_ma_hoa.split(',')
    van_ban_giai_ma = ''
    for c in van_ban_ma_hoa:
        c = int(c)
        m = pow(c, d, n)
        van_ban_giai_ma += chr(m)
    return van_ban_giai_ma

def tao_khoa_rieng_tu_p_q(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (n, d)

def nguoi_nghe_len():
    from scapy.all import sniff, Raw
    print("Người nghe lén: Đang bắt gói tin...")
    def xu_ly_goi_tin(packet):
        try:
            if packet.haslayer(Raw):
                payload = packet[Raw].load.decode('utf-8')
                chuoi_pem, van_ban_ma_hoa = payload.split('||')
                print("Người nghe lén: Đã bắt được chuỗi PEM và văn bản mã hóa.")
                print(f"Chuỗi PEM bắt được:\n{chuoi_pem}")
                print(f"Văn bản mã hóa bắt được: {van_ban_ma_hoa}")

                print("\nNgười nghe lén: Đang chuyển đổi chuỗi PEM thành khóa công khai...")
                khoa_cong_khai = pem_sang_khoa_cong_khai(chuoi_pem)
                print(f"Khóa công khai: {khoa_cong_khai}")

                print("\nNgười nghe lén: Đang chạy thuật toán Shor để tìm p, q...")
                n, e = khoa_cong_khai
                factors = chay_thuat_toan_shor(n)
                if factors:
                    p, q = factors
                    print(f"Thừa số tìm được: [{p}, {q}]")
                    print("\nNgười nghe lén: Đang tạo khóa riêng từ p, q...")
                    khoa_rieng = tao_khoa_rieng_tu_p_q(p, q, e)
                    print(f"Khóa riêng: {khoa_rieng}")

                    print("\nNgười nghe lén: Đang giải mã văn bản...")
                    van_ban_giai_ma = giai_ma_rsa(van_ban_ma_hoa, khoa_rieng)
                    print(f"Văn bản giải mã: {van_ban_giai_ma}")
                else:
                    print("Người nghe lén: Không tìm được thừa số sau nhiều lần thử!")
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi xử lý gói tin: {e}")
            return False

    try:
        packets = sniff(filter="tcp port 1234", count=1, stop_filter=xu_ly_goi_tin)
    except Exception as e:
        print(f"Lỗi khi bắt gói tin: {e}")

if __name__ == "__main__":
    nguoi_nghe_len()