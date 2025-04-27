import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 45000

def handle_request(conn, addr):
    print(f"Terhubung dengan {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                request = data.decode('utf-8').strip()
                print(f"Request dari {addr}: {request}")

                if request.startswith("TIME"):
                    now = datetime.now()
                    waktu = now.strftime("%d %m %Y %H:%M:%S")
                    response = f"JAM {waktu}\r\n"
                    conn.sendall(response.encode('utf-8'))
                elif request == "QUIT":
                    print(f"{addr} meminta keluar.")
                    break
                else:
                    print(f"Permintaan tidak dikenal dari {addr}: {request}")
            except Exception as e:
                print(f"Error pada {addr}: {e}")
                break
    print(f"Koneksi dengan {addr} ditutup.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server berjalan di {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_request, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer dimatikan.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
