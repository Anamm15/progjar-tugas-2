import socket

SERVER_IP = '172.16.16.101'
SERVER_PORT = 45000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            print(f"Terhubung ke server {SERVER_IP}:{SERVER_PORT}")
            
            while True:
                pesan = input("Ketikkan perintah (TIME/QUIT): ").strip()
                if not pesan:
                    continue

                s.sendall((pesan + '\r\n').encode('utf-8'))
                
                if pesan == "QUIT":
                    print("Keluar dari server.")
                    break

                data = s.recv(1024)
                if not data:
                    print("Server memutus koneksi.")
                    break

                print("Dari server:", data.decode('utf-8').strip())

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
