import socket
import threading

VPS_HOST = '0.0.0.0'
VPS_PORT = 1234
tunnel_socket = None

def handle_external_connection(client_socket):
    global tunnel_socket
    if not tunnel_socket:
        print("[VPS] Chưa có PC nào kết nối đến Server")
        client_socket.close()
        return

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

    threading.Thread(target=forward, args=(client_socket, tunnel_socket)).start()
    threading.Thread(target=forward, args=(tunnel_socket, client_socket)).start()

def listen_for_external_connections():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((VPS_HOST, VPS_PORT))
    server_socket.listen(5)
    print(f"[VPS] Đang lắng nghe trên {VPS_HOST}:{VPS_PORT} cho các kết nối từ bên ngoài...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[VPS] Kết nối mới từ {addr}")
        threading.Thread(target=handle_external_connection, args=(client_socket,)).start()

def listen_for_pc_connection():
    global tunnel_socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(('0.0.0.0', 5555))
    listen_socket.listen(1)
    print("[VPS] Đang lắng nghe kết nối từ PC trên cổng 5555...")

    while True:
        tunnel_socket, addr = listen_socket.accept()
        print(f"[VPS] PC đã kết nối từ {addr}")

if __name__ == "__main__":
    threading.Thread(target=listen_for_pc_connection).start()
    threading.Thread(target=listen_for_external_connections).start()