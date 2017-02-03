#!/usr/bin/python2

from socket import *

server_port = 12000
server_name = 'localhost'
message_size = 1024 # in bytes

print 'server port ', server_port
print 'server name ', server_name

# Create a server socket, bind it to a port and start listening
handshake_socket = socket(AF_INET, SOCK_STREAM)
handshake_socket.bind(('', server_port))
handshake_socket.listen(1)

while True:
    # Start receiving data from the client
    print 'Ready to serve...'

    client_socket, client_address = handshake_socket.accept()

    print 'Received a connection from:', client_address

    message = client_socket.recv(message_size)

    print '---------------------------------------------------------'
    print 'Received -> \n', message[:]
    print '---------------------------------------------------------'

    # Extract the filename from the given message
    if len(message) > 0:
        print message.split()[1]
        filename = message.split()[1].partition("/")[2]
        filename = filename[1:len(filename)-1]
        file_exists = False
        #filetouse = "/" + filename TODO: reenable
        print 'file = ', filename

        try:
            # Check wether the file exist in the cache
            #f = open(filetouse[1:], "r") TODO: reenable
            file = open(filename, "r")

            file.readlines()
            file_exists = True

            # ProxyServer finds a cache hit and generates a response message
            client_socket.send("HTTP/1.0 200 OK\r\n")
            client_socket.send("Content-Type:text/html\r\n")
            client_socket.send(file.read())

        # Error handling for file not found in cache
        except IOError:
            if not file_exists:
                # Create a socket on the proxyserver
                proxy_server_socket = '' # TODO Fill in start.                               # Fill in end.
                hostname = filename.replace("www.", "", 1)
                print hostname
                try:
                    # Connect to the socket to port 80
                    # TODO Fill in start.
                    # Fill in end.
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    file_object = proxy_server_socket.makefile('r', 0)
                    file_object.write("GET " + "http://" + filename + " HTTP / 1.0\n\n")
                    # Read the response into buffer
                    # TODO Fill in start.
                    # Fill in end.
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket
                    # and the corresponding file in the cache
                    temp_file = open("./" + filename, "wb")
                    # TODO Fill in start.
                    # Fill in end.
                except:
                    print "Illegal request"
            else:
                # HTTP response message for file not found
                print 'file not found'
                # TODO Fill in start.
                # Fill in end.

    # Close the client and the server sockets
    client_socket.close()

# TODO Fill in start.
# Fill in end.
