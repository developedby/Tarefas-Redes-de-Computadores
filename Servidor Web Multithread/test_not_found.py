import socket
serverName = "localhost"
serverPort = 1973 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName,serverPort)) 
request = "GET /secret.htm HTTP/1.0\n"
s.send(request.encode('ascii'))
response = s.recv(1024) 
print("HTTP response received: ") 
print(response)
s.close()
