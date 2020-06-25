import socket
import select

'''The main part of the server side is the select module which iterates 
    over the clients for checking the incoming strings to the server.
    The core work is totally done by the select module.'''
class ChatServer:
    def __init__( self, port ):
        self.port = port
        # server socket is created belonging to ipv4 family using stream socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this line allows the server to connect to the client if it gets disconnected due to any reason
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # binding of the port to the host is taking place
        self.serversocket.bind(("", port))
        # here the server listens to maximum 5 clients and it can b changed as per requirement
        self.serversocket.listen(5)
        # a list is been initialised which keeps track of the clients which are connected to the server
        self.socket_addresses_lst = [self.serversocket]
        print('ChatServer started on port %s' % port)

# the main def "run" takes care of the whole program which is going to be executed
    def run(self):

        while 1:
            # Await an event on a readable socket descriptor
            # select method returns 3 lists which consist of reading, writing and exception handling cases
            (sread, swrite, sexc) = select.select(self.socket_addresses_lst, [], [])
            # Iterate through the tagged read descriptors
            for sock in sread:
                # Received a connect to the server (listening) socket
                if sock == self.serversocket:
                    self.accept_new_connection()
                else:
                    # Received something on a client socket
                    recv_string = sock.recv(100)
                    # the string is converted from byte string to normal string
                    recv_string = recv_string.decode('utf-8')
                    # Check to see if the peer socket closed
                    if recv_string == '':
                        host, port = sock.getpeername()
                        recv_string = 'Client left %s:%s\r\n' % (host, port)
                        self.send_string_all(recv_string, sock)
                        sock.close()
                        self.socket_addresses_lst.remove(sock)
                    else:
                        host, port = sock.getpeername()
                        newstr = '[%s:%s] %s' % (host, port, recv_string)
                        self.send_string_all(newstr, sock)



    def send_string_all(self, string, omit_sock):
        for sock in self.socket_addresses_lst:
            # it send s the string entered by the client to the remaining clients except the one who has sent it
            if sock != self.serversocket and sock != omit_sock:
                sock.sendall((string+'\r\n').encode())

        print(str(string))

    def accept_new_connection(self):
        newsocket, (remhost, remport) = self.serversocket.accept()
        self.socket_addresses_lst.append(newsocket)
        welcome_string= "You're connected to the Python chatserver\r\n"
        newsocket.send(bytes(welcome_string.encode()))
        str = 'Client joined %s:%s\r\n' % (remhost, remport)
        self.send_string_all(str, newsocket)


myServer = ChatServer(9595)
myServer.run()