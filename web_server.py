# Mengimport modul socket yang digunakan untuk komunikasi jaringan
import socket
# Mengimport modul os untuk melakukan operasi pada sistem operasi seperti memeriksa keberadaan file
import os

# Variabel CONTENT_TYPES adalah dictionary yang berisi jenis-jenis konten dan file extension
CONTENT_TYPES = {
    "application": {
        'pdf': 'application/pdf'
    },
    "text": {
        'html': "text/html",
        'css': "text/css",
        'js': "text/javascript"
    },
    "video": {
        'mp4': "video/mp4"
    },
    "image": {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',

    },
    "audio": {
        'mp3': 'audio/mpeg'
    }

}


# fungsi parse_request digunakan untuk mem-parse request HTTP dari client dan mengembalikan method dan file_path yang diminta
# dengan parameter request.
def parse_request(request):
    # Mem-parse HTTP request
    request_parts = request.split()

    # default dari parse request yang diminta
    file_path = "index.html"
    method = "GET"

    # Mengecek apakah permintaan tidak kosong.
    if len(request_parts) != 0:
        method = request_parts[0]  # mengambil method yang di kirimkan
        file_path = request_parts[1][1:]  # menghilangkan leading slash '/'

        # Menyimpan jalur file dari permintaan dengan menghapus garis miring awal ("/") jika ada.
        if file_path == "":
            file_path = "index.html"

    # Mengembalikan method dan file path
    return method, file_path


# Fungsi create_response digunakan untuk membuat respons HTTP berdasarkan jalur file yang diminta dan metode HTTP yang
# diterima dengan parameter file_path dan method.
def create_response(file_path, method):
    # Jika metode adalah 'GET', maka mencari file yang diminta oleh client.
    if method == 'GET':
        # Jika file ditemukan, membuka file dan membuat respons HTTP dengan header dan konten file yang sesuai.
        if os.path.exists(file_path):
            # mengakses variable content_types untuk melakukan pengecekan terhadap file extension dengan membaginya
            # menjadi key dan value
            for key, value in CONTENT_TYPES.items():
                # melakukan pengecekan pada file_path apakah ada di value
                if file_path.split('.')[-1] in value:
                    # membuka file jika file extension tersebut ada
                    with open(file_path, 'rb') as file:
                        # Membuat response message dengan header HTTP dan konten file diminta
                        return f"HTTP/1.1 200 OK\nContent-Type: {CONTENT_TYPES[key][file_path.split('.')[-1]]}\n\n".encode(
                        ) + file.read()

        # Jika file tidak ditemukan, membuka file "404.html" dan membuat respons HTTP dengan pesan '404 Not Found'.
        else:
            # Membuat response message dengan pesan '404 Not Found'
            with open("404.html", 'rb') as file:
                # Membuat response message dengan header HTTP dan konten file gambar yang diminta
                return f"HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n".encode() + file.read()

    # Jika metode bukan 'GET', maka membuat respons HTTP dengan pesan '405 Method Not Allowed'.
    else:
        # Membuat response message dengan pesan '405 Method Not Allowed'
        return "HTTP/1.1 405 Method Not Allowed\n\n405 Method Not Allowed".encode()


# Fungsi run_web_server digunakan untuk menjalankan web server dengan parameter host dan port
def run_web_server(host, port):
    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Mengikat socket ke alamat dan port tertentu
    server_socket.bind((host, port))
    # Menerima koneksi dari client
    server_socket.listen(1)
    # Selama server berjalan, menerima koneksi dari client, menerima permintaan dari client, mem-parse permintaan,
    # membuat respons, dan mengirimkan respons ke client.
    print(f"Server berjalan di http://{host}:{port}")

    while True:
        # Menerima koneksi dari client
        client_socket, client_address = server_socket.accept()
        print(f"Koneksi diterima dari {client_address}")
        # Menerima request dari client
        request = client_socket.recv(1024).decode()
        print(f"Request:\n{request}")
        # memanggil fungsi parse_request
        method, file_path = parse_request(request)
        # memanggil fungsi create_response
        response = create_response(file_path, method)
        # Mengirimkan response message ke client
        client_socket.sendall(response)
        # Menutup koneksi dengan client setelah respons dikirim.
        client_socket.close()


# Memastikan bahwa skrip ini hanya dijalankan jika ini adalah file utama.
if __name__ == "__main__":
    # Memanggil fungsi run_web_server dengan parameter"localhost" sebagai host dan 8080 sebagai port untuk menjalankan server web.
    run_web_server("localhost", 8080)
