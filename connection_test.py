import socket

request = b"GET / HTTP/1.1\nHost: www.cnn.com\n\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.43.154", 80))
s.send(request)
result = s.recv(3)
while len(result) > 0:
    print(result)
    result = s.recv(3)
