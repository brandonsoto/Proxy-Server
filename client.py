#!/usr/bin/python

from socket import *

server_port = 12000
server_name = 'localhost'

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

sent_message = raw_input('message to send -> ')

print 'sending message: "', sent_message, '"'
client_socket.send(sent_message)
print 'message sent!'

print 'receiving message...'
message = client_socket.recv(1024)
print 'received "', message, '"'

client_socket.close()

print 'Client done!'

