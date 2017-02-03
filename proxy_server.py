#!/usr/bin/python

from socket import *

server_port = 12000
server_name = 'localhost'
message_size = 1024 # in bytes

print 'server port ', server_port
print 'server name ', server_name

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', server_port))
tcpSerSock.listen(1)

while True:
    # Start receiving data from the client
    print 'Ready to serve...'

    tcpCliSock, addr = tcpSerSock.accept()

    print 'Received a connection from:', addr

    message = tcpCliSock.recv(message_size)

    print '---------------------------------------------------------'
    print 'Received -> \n', message[:]
    print '---------------------------------------------------------'

    # Extract the filename from the given message
    if len(message) > 0:
        print message.split()[1]
        filename = message.split()[1].partition("/")[2]
        filename = filename[1:len(filename)-1]
        fileExist = "false"
        #filetouse = "/" + filename TODO: reenable
        print 'file = ', filename

        try:
            # Check wether the file exist in the cache
            #f = open(filetouse[1:], "r") TODO: reenable
            f = open(filename, "r")
            outputdata = f.readlines()
            fileExist = "true"
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")
            tcpCliSock.send(f.read())

        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver
                c = '' # TODO Fill in start.                               # Fill in end.
                hostn = filename.replace("www.", "", 1)
                print hostn
                try:
                    # Connect to the socket to port 80
                    # TODO Fill in start.
                    # Fill in end.
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj = c.makefile('r', 0)
                    fileobj.write("GET " + "http://" + filename + " HTTP / 1.0\n\n")
                    # Read the response into buffer
                    # TODO Fill in start.
                    # Fill in end.
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket
                    # and the corresponding file in the cache
                    tmpFile = open("./" + filename, "wb")
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
    tcpCliSock.close()

# TODO Fill in start.
# Fill in end.
