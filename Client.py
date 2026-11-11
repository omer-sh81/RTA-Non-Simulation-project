import socket
import base64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.56.1", 12345))# creates a socket with the serve, ip and port can be changed
while True:
    print("Enter any command, if you are willing to stop send exit.")
    command= input()
    s.send(base64.b64encode(command.encode()))
    if command == "exit":#if the client wishes to finish the "conversion" it will first alert the server and then close the socket
        s.close()
        break
    header = b""
    while len(header) < 10:#making sure the client got the header correctly
        header += s.recv(10 - len(header))
    header = int(header.decode("utf-8"))
    data = b""
    while header>len(data):#making sure the client got the data correctly
        data += s.recv(min(4096, header - len(data)))
    print(base64.b64decode(data).decode("utf-8"))
