import socket
from datetime import datetime
import subprocess
import os

class HttpRequestHandler:
    def __init__ (self, sckt, addr):
        self.sckt = sckt
        self.addr = addr
        self.msg = self.sckt.recv(4096).decode('ascii')
        print("Request:") #DEBUG
        print(self.msg) #DEBUG

    def handle (self):
        try:
            self.handle_get_request()
        except Exception as error:
            print(error)
            self.handle_bad_request()
        finally:
            self.sckt.close()

    def handle_get_request (self):
        self.msg = self.msg.split("\n")
        print(self.msg) #DEBUG
        print(self.msg[0]) #DEBUG
        print(self.msg[0].split(" ")[0]) #DEBUG
        if self.msg[0].split(" ")[0] != "GET":
            raise ValueError("Server currently only accepts GET requests")
        self.file_path = './files' + self.msg[0].split(" ")[1]
        print(self.file_path) #DEBUG
        try:
            self.requested_file = open(self.file_path , 'rb')
        except:
            response = self.create_404_response()
        else:
            response = self.create_200_response()
        print("Response: ") #DEBIG
        print(response)
        self.sckt.send(response)

    def create_200_response (self):
        r = "HTTP/1.0 200 OK\n"
        r += "Date: " + datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " GMT\n"
        r += "Server: gitlab.com/nicolasabril\n"
        mime_type = subprocess.getoutput('file --brief --mime ' + self.file_path)
        r += "Content-Type: " + mime_type + "\n"
        r += "Content-Length: " + str(os.stat(self.file_path).st_size) + '\n'
        modified_time = os.path.getmtime(self.file_path)
        r += "Last-Modified: " + datetime.utcfromtimestamp(modified_time).strftime("%a, %d %b %Y %H:%M:%S") + 'GMT\n\n'
        r = bytes(r, 'ascii') + self.requested_file.read()

        return r

    def create_404_response (self):
        r = "HTTP/1.0 404 FILE NOT FOUND\n"
        r += "Date: " + datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " GMT\n"
        r += "Server: gitlab.com/nicolasabril\n"
        body = "<HTML><HEAD><TITLE>404 File Not Found</TITLE></HEAD><BODY><h1>Not Found</h1><p>File " + self.msg[0].split(" ")[1] + " was not found on the server.</p></BODY></HTML>";
        r += "Content-Length: " + str(len(body)) + '\n'
        r += "Content-Type: text/html; charset=us-ascii\n\n"
        r += body
        return bytes(r, 'ascii')

    def handle_bad_request (self):
        r = "HTTP/1.X 400 BAD REQUEST\n"
        r += "Date: " + datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " GMT\n"
        r += "Server: gitlab.com/nicolasabril\n"
        body = "<HTML>\n<HEAD>\n<TITLE>300 Bad Request</TITLE>\n</HEAD>\n<BODY>\n<h1>Bad Request</h1>\n<p>The request received was not understood by the server.</p>\n</BODY>\n</HTML>\n";
        r += "Content-Length: " + str(len(body)) + '\n'
        r += "Content-Type: text/html; charset=us-ascii\n\n"
        r += body
        self.sckt.send(bytes(r, 'ascii'))


def handle_http_request (sckt, addr):
    request_handler = HttpRequestHandler(sckt, addr)
    request_handler.handle()

