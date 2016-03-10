import socket
import sys
import argparse
import time

host = 'localhost'


def echo_client(port):
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)

    print "connecting to the  echo server on %s port %s"%server_address
    # sock.bind(server_address)
    # sock.listen(backlog)
    sock.connect(server_address)

    try:
        message = "Test message sent at %d"%time.time()
        print "sneding %s"%message
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)            
            print "received :%s"%data
    except socket.error,e:
        print "socket error %s"%str(e)
    except Exception,e:
        print "other exception :%s"%str(e)
    finally:
        print "closing connection to the server"
        sock.close()
    # while 1:
    #     print "waitting to reveive message from client"
    #     client,address =sock.accept()
    #     data = client.recv(data_payload)
    #     if data:
    #         print "Data:%s"%data
    #         client.send("i receive your message:%s"%data)
    #         print "sent %s bytes back to %s"%(data,address)
    #     client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='socket server example')
    parser.add_argument('--port',action='store',dest='port',type=int,required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)
