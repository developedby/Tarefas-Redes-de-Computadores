import socket

def solve_http_request (sckt, addr):
    msg = sckt.recv(4096).decode('ascii')
    if (is_get_request(msg)):
        solve_get_request(msg, sckt, addr)
    else:
        send_bad_request_response(sckt, addr)
    sckt.close()

def is_get_request(msg):
    pass

def solve_get_request(msg, sckt, addr):
    pass

def send_bad_request_response(sckt, addr):
    pass
