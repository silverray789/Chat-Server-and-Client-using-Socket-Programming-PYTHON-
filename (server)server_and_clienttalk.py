import socket
import sys

def create_socket():
    try:

        global host
        global port
        global s

        host=''
        port=9595
        print('socket created with port :- ',str(port))
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print('socket creation error:-  ',str(msg))


def bind_socket():
    try:
        global host
        global port
        global s

        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print('socket binding error :- ',str(msg))
        bind_socket()

def accept_socket():
    try:
        conn,address=s.accept()
        print('connecting socket to IP address :- ',str(address[0]),'  and port number :- ',str(address[1]))
        send_commands(conn)
        conn.close()
    except:
        print('<<<Connection lost with the Client..!!>>>')



def send_commands(conn):
    if conn:
        conn.send(str.encode('Welcome to the chat Server'))
        while 1:
            cmd=input('Server-> ')
            if len(str.encode(cmd))>0:
                cmd = 'Server-> ' + cmd+'\n'
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(1024),'utf-8')
                print('\n'+client_response,end='\n')
    else:
        print('No connection received..!!')




def main():
    create_socket()
    bind_socket()
    accept_socket()

main()



