import socket
serverName = "localhost"
serverPort = 1973 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName,serverPort)) 
request = "ASGHADIAJDGISDIGAEURGIRUGAPSDUASERT#$%TE$GFW#%*rtg8tgw34ty8ue45y8905uyh"
s.send(request.encode('ascii'))
response = s.recv(1024) 
print("HTTP response received: ") 
print(response)
s.close()
