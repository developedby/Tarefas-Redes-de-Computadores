import threading
import socket
from sys import exit as sys_exit
import http_request


port = 1973
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', port))
server_socket.listen()

try:
    while True:
        connection_socket, connection_addr = server_socket.accept()
        request_thread = threading.Thread(target=http_request.handle_http_request, args=(connection_socket, connection_addr))
        request_thread.start()
except:
    server_socket.close()
    try:
        connection_socket.close()
    except:
        pass
    print("\n\nExiting by interupt...")
    sys_exit(0)
