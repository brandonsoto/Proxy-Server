#!/usr/bin/env python

# Thanks to Luu Thuy (http://luugiathuy.com/2011/03/simple-web-proxy-python)
# This was adapted from yous.

import os, sys, thread, socket

### Constants
MAX_CONNECTIONS = 100
MAX_MSG_SIZE    = 9999999
SERVER_NAME     = 'localhost'
SERVER_PORT     = 4242
DEFAULT_PORT    = 80


def main():
    print "Server running on", SERVER_NAME, ":", SERVER_PORT

    # create TCP socket for handshake with clients
    handshake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        handshake_socket.bind((SERVER_NAME, SERVER_PORT))
        handshake_socket.listen(MAX_CONNECTIONS)

    except socket.error, (value, message):
        if handshake_socket:
            handshake_socket.close()
        print "Could not open socket:", message
        sys.exit(1)

    # get the connection from client
    while True:
        client_connection, client_address = handshake_socket.accept()

        print 'Server now connected with ', client_address

        # create a thread to handle request
        thread.start_new_thread(proxy_thread, (client_connection, client_address))

    handshake_socket.close()
    print "\033[", 39, "m", "Server done!\033m[0m"
### end of main


def print_to_console(http_method, request, address):
    color_code = 39

    if "Request" in http_method:
        color_code = 96 # light cyan
    elif "Reset" in http_method:
        color_code = 33 # yellow
    elif 'Get' in http_method:
        color_code = 32 # green

    print 'http_method =', http_method

    print "\033[", color_code, "m", address[0], "\t", http_method, "\t", request, "\033[0m"
### end of print_to_console


def close_socket(socket):
    if socket:
        socket.close()
        print "\033[", 91, "m", "Closed ", socket.getsockname(), " socket\033[0m"
### end of close_socket


# extracts the webserver's name and port from the given url
# returns (0=webserver name, 1=webserver_port)
def extract_webserver_data(url):
    http_position = url.find("://")  # find pos of ://
    webserver_string = ''

    if (http_position == -1):
        webserver_string = url
    else:
        webserver_string = url[(http_position + 3):]  # get the rest of url

    port_position = webserver_string.find(":")  # find the port pos (if any)

    # find end of web server
    server_position = webserver_string.find("/")

    if server_position == -1:
        server_position = len(webserver_string)

    webserver_name = ""
    webserver_port = -1

    if (port_position == -1 or server_position < port_position):  # default port
        webserver_port = DEFAULT_PORT
        webserver_name = webserver_string[:server_position]
    else:                                                         # specific port
        webserver_port = int((webserver_string[(port_position + 1):])[:server_position - port_position - 1])
        webserver_name = webserver_string[:port_position]

    return (webserver_name, webserver_port)
### end of extract_webserver_data


def proxy_thread(client_socket, client_address):
    browser_request = client_socket.recv(MAX_MSG_SIZE)
    try:
        request_line = browser_request.split('\n')[0]
        url = request_line.split(' ')[1]

        print_to_console("Request", request_line, client_address)

        webserver_data = extract_webserver_data(url)
        webserver_name = webserver_data[0]
        webserver_port = webserver_data[1]

        # create a TCP socket to connect this proxy to the web server
        webserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            webserver_socket.connect((webserver_name, webserver_port))
            webserver_socket.send(browser_request)  # forward request to webserver

            while True:
                data = webserver_socket.recv(MAX_MSG_SIZE) # receiver data from webserver
                if (len(data) > 0):
                    client_socket.send(data) # forward received message to browser
                else:
                    break
            webserver_socket.close()
            client_socket.close()

        except socket.error, (value, message):
            if webserver_socket:
                webserver_socket.close()
            if client_socket:
                client_socket.close()
            print_to_console("Peer Reset", request_line, client_address)
            sys.exit(1)
    except IndexError:
        print 'index error occurred'
        if client_socket:
            client_socket.close()
### end of proxy thread

if __name__ == '__main__':
    main()
