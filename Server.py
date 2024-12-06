import socket
import subprocess
import os
import base64

print("Selamat datang di Remote Termux!")
print("Kode ini dibuat untuk mempermudah penggunaan,")
print("sehingga dapat membantu memasukkan kode secara efisien.")
print("Dan menciptakan kompatibilitas serta pengalaman yang baik.")
print("Kode ini dibuat oleh: ExDicer")

def main():
    # Input konfigurasi
    HOST = input("Masukkan alamat IP server: ")
    PORT = int(input("Masukkan port server: "))

    try:
        # Membuat socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        print(f"Menunggu koneksi di {HOST}:{PORT}...")

        conn, addr = sock.accept()
        print(f"Terhubung dengan {addr}")

        cwd = os.getcwd()

        while True:
            # Menerima perintah
            perintah = base64.b64decode(conn.recv(1024)).decode()

            if perintah == "keluar":
                break

            try:
                # Menjalankan perintah
                if perintah.startswith("cd "):
                    os.chdir(perintah[3:])
                    cwd = os.getcwd()
                    hasil = f"Directory sekarang: {cwd}"
                else:
                    hasil = subprocess.check_output(perintah, shell=True, stderr=subprocess.STDOUT).decode()
            except subprocess.CalledProcessError:
                hasil = "Kesalahan: Perintah tidak dikenal"

            hasil_encode = base64.b64encode(hasil.encode())
            conn.send(hasil_encode)

    except (ConnectionAbortedError, ConnectionRefusedError) as e:
        if isinstance(e, ConnectionAbortedError):
            print("Koneksi client ditutup.")
        elif isinstance(e, ConnectionRefusedError):
            print("Koneksi ke server ditolak.")
    except Exception as e:
        print(f"Kesalahan: {e}")
    finally:
        # Menutup koneksi
        try:
            conn.close()
            sock.close()
        except:
            pass

if __name__ == "__main__":
    main()
