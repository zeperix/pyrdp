import socket
import threading
import time
import sys

LOCAL_HOST = '127.0.0.1'

if len(sys.argv) < 4:
    print("<<<Thiếu dữ liệu>>>\nCách sử dụng: python user.py [Local port] [IP Server] [Server Port]\nGiải thích:\n -[Local port]: Cổng trên thiết bị hiện tại, dữ liệu sẽ truyền qua cổng này\n -[IP Server]: IP của máy chủ chuyển tiếp trung gian\n -[Server Port]: Cổng của máy chủ chuyển tiếp trung gian")
    sys.exit(1)

try:
    LOCAL_PORT = int(sys.argv[1])      
    VPS_HOST = sys.argv[2]            
    VPS_PORT = int(sys.argv[3])        
except ValueError:
    print("Lỗi: Vui lòng nhập số nguyên [Local port] và [Server Port]")
    sys.exit(1)

print(f"Cổng cục bộ: {LOCAL_PORT}")
print(f"IP Server: {VPS_HOST}")
print(f"Port Server: {VPS_PORT}")

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except:
        pass
    finally:
        source.close()
        destination.close()

def handle_vps_connection(vps_socket):
    try:
        # Tạo kết nối tới dịch vụ cục bộ
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_socket.connect((LOCAL_HOST, LOCAL_PORT))
        print("[PC] Đã thiết lập kết nối với cổng cục bộ\nSẵn sàng ")

        # Chuyển tiếp dữ liệu giữa VPS và dịch vụ cục bộ
        thread1 = threading.Thread(target=forward, args=(vps_socket, local_socket))
        thread2 = threading.Thread(target=forward, args=(local_socket, vps_socket))

        thread1.start()
        thread2.start()

        # Chờ cho đến khi cả hai luồng kết thúc
        thread1.join()
        thread2.join()

    except Exception as e:
        print(f"[PC] Lỗi kết nối với cổng cục bộ: {e}")
    finally:
        vps_socket.close()
        print("[PC] Kết nối tới Server đã bị ngắt")

def connect_to_vps():
    while True:
        try:
            # Kết nối tới VPS
            vps_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            vps_socket.connect((VPS_HOST, VPS_PORT))
            print("[PC] Đã thiết lập kết nối với Server")

            # Xử lý kết nối chuyển tiếp
            handle_vps_connection(vps_socket)

        except Exception as e:
            print(f"[PC] Kết nối với Server thất bại: {e}. Thử lại sau 5 giây...")
            time.sleep(5)

if __name__ == "__main__":
    connect_to_vps()
