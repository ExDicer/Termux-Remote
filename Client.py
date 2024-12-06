import socket
import base64

def main():
    # Input konfigurasi
    HOST = input("Masukkan alamat IP server: ")
    PORT = int(input("Masukkan port server: "))

    try:
        # Membuat socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"Terhubung dengan {HOST}:{PORT}!")

        while True:
            # Mengirim perintah
            perintah = input("Masukkan perintah: ")

            perintah_encode = base64.b64encode(perintah.encode())
            sock.send(perintah_encode)

            # Menerima hasil
            hasil_encode = sock.recv(1024)
            hasil = base64.b64decode(hasil_encode).decode()
            print(hasil)

            if perintah == "keluar":
                break

    except (ConnectionAbortedError, ConnectionRefusedError) as e:
        if isinstance(e, ConnectionAbortedError):
            print("Koneksi server ditutup.")
        elif isinstance(e, ConnectionRefusedError):
            print("Koneksi ke server ditolak.")
    except Exception as e:
        print(f"Kesalahan: {e}")
    finally:
        # Menutup koneksi
        try:
            sock.close()
        except:
            pass

if __name__ == "__main__":
    main()
