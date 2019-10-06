from socket import *
import ssl
import base64

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

recipient = "<USER@mail.uc.edu>"
sender = "<USER@gmail.com>"
username = "USER@gmail.com"
password = "PASSWORD"

# Using SMTP port on gmail server
servername = "smtp.gmail.com"
mailserver = (servername, 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
	print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# STARTTLS command to begin connection with gmail server
tlsCommand = 'STARTTLS\r\n'
clientSocket.send(tlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('250 reply not received from server.')

#Encrypt connection
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname = servername)

# Send the AUTH LOGIN command and print server response.
authCommand = 'AUTH LOGIN\r\n'
clientSocket.write(authCommand.encode())
recv3 = clientSocket.read(1024).decode()
print(recv3)
if recv3[:3] != '334':
	print('334 reply not received from server')

#Send username
uname = base64.b64encode(username.encode())
endline = '\r\n'
uname = uname + endline.encode()
clientSocket.write(uname)
recv4 = clientSocket.read(1024).decode()
print(recv4)
if recv4[:3] != '334':
	print('334 reply not received from server')

#Send password
pswrd = base64.b64encode(password.encode())
pswrd = pswrd + endline.encode()
clientSocket.write(pswrd)
recv5 = clientSocket.read(1024).decode()
print(recv5)
if recv5[:3] != '235':
	print('235 reply not received from server')
    
# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: " + sender + "\r\n"
clientSocket.send(mailFrom.encode())
recv6 = clientSocket.read(1024).decode()
print("After MAIL FROM command: "+recv6)
if recv6[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response. 
rcptTo = "RCPT TO: " + recipient + "\r\n"
clientSocket.send(rcptTo.encode())
recv7 = clientSocket.recv(1024).decode()
print("After RCPT TO command: "+recv7)
if recv7[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv8 = clientSocket.recv(1024).decode()
print("After DATA command: "+recv8)
if recv8[:3] != '354':
    print('354 reply not received from server.')
    
# Send message data.
clientSocket.write(msg.encode())

# Message ends with a single period.
clientSocket.write(endmsg.encode())
recv9 = clientSocket.read(1024).decode()
print("After endmsg command: " + recv9)
if recv9[:3] != '250':
	print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.write(quitCommand.encode())
recv10 = clientSocket.read(1024).decode()
print("After QUIT command: " + recv10)
if recv10[:3] != '221':
	print('221 reply not received from server.')

clientSocket.close()
