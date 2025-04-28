import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 45000
    
class ProcessTheClient(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):
        print(f"Terhubung dengan {self.addr}")
        buffer = ""
        while True:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break
                
                buffer += data.decode('utf-8')
                if not buffer.endswith('\r\n'):
                    continue
                
                request = buffer[:-2]
                print(f"Request dari {self.addr}: {request}")
                
                if request.startswith("TIME"):
                    now = datetime.now()
                    waktu = now.strftime("%d %m %Y %H:%M:%S")
                    response = f"JAM {waktu}\r\n"
                    self.conn.sendall(response.encode('utf-8'))
                elif request == "QUIT":
                    print(f"{self.addr} meminta keluar.")
                    break
                else:
                    print(f"Permintaan tidak dikenal dari {self.addr}: {request}")      
                    
                buffer = ""
            except Exception as e:
                print(f"Error pada {self.addr}: {e}")
                break
        print(f"Menutup koneksi dengan {self.addr}")
        self.conn.close()
    
class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        self.the_clients = []
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server berjalan di {self.host}:{self.port}")
        while True:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Terhubung dengan {addr}")
                
                client_thread = ProcessTheClient(conn, addr)
                client_thread.start()
                self.the_clients.append(client_thread)
                
                print(f"Jumlah klien aktif: {len(self.the_clients)}")
            except Exception as e:
                print(f"Error menerima koneksi: {e}")

def main():
    try:
        server = Server(HOST, PORT)
        server.start()
    except Exception as e:
        print(f"\nGagal untuk memulai server. Error: {e}")

if __name__ == "__main__":
    main()
