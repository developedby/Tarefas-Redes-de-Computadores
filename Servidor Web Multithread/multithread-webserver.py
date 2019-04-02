import threading
import socket



port = 1405
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', port))
server_socket.listen()

while True:
    connection_socket, connection_addr = server_socket.accept()
    request_thread = threading.Thread(target=solve_http_request, args=(connection_socket, connection_addr))
    request_thread.start()
