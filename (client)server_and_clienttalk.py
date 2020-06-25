import socket


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=9595
s.connect((host,port))


while 1:
    data=s.recv(1024)
    if data.decode() == 'Welcome to the chat Server':
        print('Welcome to the chat Server')
        print('Wait for the Server to message first....')
    if data.decode()!='Welcome to the chat Server':
        cmd=data[:].decode("utf-8")
        print('\n'+cmd)
        msg=input('Client-> ')
        msg='Client-> '+msg+'\n'
        s.send(msg.encode())





