#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
host = gethostbyname(gethostname())
serverSocket.bind((host, 80))
serverSocket.listen(1)

print("Listening at ", host, "...")

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()          
    try:
        message = connectionSocket.recv(1024)               
        filename = message.split()[1]                 
        f = open(filename[1:])                        
        outputdata = f.read()
        f.close()
        
    #Send one HTTP header line into socket
        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())
                  
        
    #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
        
    except IOError:
    #Send response message for file not found
        header = "HTTP/1.1 404 Not Found\r\n\r\n"
        message = ("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        connectionSocket.send(header.encode())
        connectionSocket.send(message.encode())
        connectionSocket.close()

        
serverSocket.close()
