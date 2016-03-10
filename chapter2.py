#coding=utf-8
import os
import time
import socket
import threading 
import SocketServer

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = '\nhello,world at %d \n'%time.time()

class ForkingClient():
    def __init__(self,ip,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((ip,port))

    def run(self):
        current_process_id = os.getpid()
        print 'PID%s Sending echo message to the server:\n'%current_process_id\
              +'%s'%ECHO_MSG
        sent_data_length = self.sock.send(ECHO_MSG)
        print 'Sent:%d characters,so far...\n'%sent_data_length

        response = self.sock.recv(BUF_SIZE)
        print 'PID %s received:%s'%(current_process_id,response[5:])

    def shutdown(self):
        self.sock.close()

class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        #send the echo back to the client
        data = self.request.recv(BUF_SIZE)        
        current_process_id = os.getpid()
        response = 'receive %s from %s at %d\n'%(current_process_id,data,time.time())
        print r'Server sending response [%s]'%response

        self.request.send(response)
        return

class ForkingServer(SocketServer.ForkingMixIn,SocketServer.TCPServer,):
    pass

def main():
    server = ForkingServer((SERVER_HOST,SERVER_PORT),ForkingServerRequestHandler)
    ip,port = server.server_address
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print 'Server loop runing PID:%s'%os.getpid()

    client1 = ForkingClient(ip,port)
    client1.run()
    
    client2 = ForkingClient(ip,port)
    client2.run()

    client3 = ForkingClient(ip,port)
    client3.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    client3.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()