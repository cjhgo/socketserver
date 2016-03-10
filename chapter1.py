#coding=utf-8
import sys
import socket

def execute_all_function():
    # this_module = sys.modules[__name__]
    import __main__
    for item in dir(__main__):
            object = getattr(__main__,item)
            if callable(object):
                if object.func_name == 'execute_all_function':
                    continue
                print '-------%s------'%object.func_name
                object()
                print '-------%s-------\n' % ('-'*len(object.func_name))


def _1_2_print_machine_info_():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print "Host name :%s" %host_name
    print "IP address :%s" % ip_address

def _1_3_get_remote_machine_info_():
    remote_host = 'www.baidu.com'
    try:
        print "IP address:%s" % socket.gethostbyname(remote_host)
    except socket.error,err_msg:
        print "%s:%s" %(remote_host,err_msg)

def _1_4_convert_ip4_address_():
    for ip_addr in ['127.0.0.1','192.168.10.1']:
        from binascii import hexlify
        packed_ip_addr = socket.inet_aton(ip_addr)
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print "IP address :%s=> Packed:%s,Unpacked:%s"\
                %(ip_addr,hexlify(packed_ip_addr),unpacked_ip_addr)

def _1_5_find_service_():
    """
    understand the network
    service :application layer
    tcp/upd "net layer
    service ::= tcp/upd+port
    一个服务运行在远程服务器的哪个端口上,采用什么协议,tcp还是upd
    一个tcp连接是一个五元组,
    client IP address, client port number, server IP address, server port number, protocol
    由于协议默认是tcp所以也可以说是四元组
    """
    protocolname = ''
    for port in [80,25]:
        print "Port:%s=> service name :%s"%(port,socket.getservbyport(port,protocolname))
def _1_6_byte_order():
    data = 1234
    #deciaml:1234
    #binary:0000 0000 0000 0000 0000 0100 1101 0010
    #hex:   0    0    0    0    0    4    d     2  ::= 00 00 04 d2
    #socket.htonl(1234)::= 0xd2 04 00 00
    #字节序发生了改变从0x000004d2 变成了0xd2040000
    print "original :%s=>Long host byte order :%s Network byte order :%s" \
             % (data,socket.ntohl(data),socket.htonl(data))

def _1_7_test_socket_timeout():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "Default socket timeout:%s" % s.gettimeout()
    s.settimeout(100)
    print "Current socket timeout:%s" % s.gettimeout()

def _1_8_handle_socket_error():
    host = '138.128.223.36'
    port = 80
    filename = 'index.html'

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,e:
        print "Error creating socket:%s"% e
        sys.exit(1)

    try:
        s.connect((host,port))
    except socket.gaierror,e:
        print "Connection error:%s"%e
        sys.exit(1)

    try:
        s.sendall("GET %s HTTP/1.1\r\n\r\n" % filename)
    except socket.error,e:
        print "Error sending data:%s"% e
        sys.exit(1)


    while 1:
        try:
            buf = s.recv(2048)
        except socket.error,e:
            print "Error receiving data:%s"% e
            sys.exit(1)
        if not len(buf):
            break
        sys.stdout.write(buf)

def _1_9_modify_buff_size():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    bufsize = sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
    print "buffer size [before]:%d"% bufsize

    sock.setsockopt(socket.SOL_TCP,socket.TCP_NODELAY,1)
    sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_SNDBUF,
            4096
        )
    sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_RCVBUF,
            4096
        )

    bufsize = sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
    print "buffer size [after]:%d"% bufsize

# def _1_10_test_socket_modes():
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     s.setblocking(1)
#     s.settimeout(0.5)
#     s.bind(("127.0.0.1",0))

#     socket_address = s.getsockname()
#     print "trivial server launched on socket:%s"% str(socket_address)
#     while 1:
#         s.listen(1)        

# def _1_11_resue_socket_addr():
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#     old_state = s.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
#     print "old sock state:%s" %old_state

#     s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#     new_state = s.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
#     print "new sock state:%s" %new_state

#     local_port = 8288

#     srv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#     srv.bind(('',local_port))
#     srv.listen(1)
#     print ("Listening on port :%s"% local_port)
#     while 1:
#         try:
#             connection,addr = srv.accept()
#             print "connected by %s:%s"% (addr[0],addr[1])
#         except KeyboardInterrupt:
#             break
#         except socket.error,msg:
#             print "%s"%msg


def _1_12_use_ntp():
    """
    ntp:network time protocol
    """
    pass

def _1_13_sntp_client():
    NTP_SERVER = '0.asia.pool.ntp.org'
    TIME1970 = 2208988800L
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = '\x1b'+47*'\0'
    client.sendto(data,(NTP_SERVER,123))
    data,address = client.recvfrom(1024)

    if data:
        print "response received from :",address
    import struct
    t = struct.unpack('!12I',data)[10]
    t  -= TIME1970
    import time
    print '\tTime=%s'%time.ctime(t)

# def _1_14_echo_server():
    
    

if __name__ == '__main__':
        # print_machine_info_1_2()
        # get_remote_machine_info_1_3()
        # convert_ip4_address_1_4()
        # find_service_1_5()
        # byte_order_1_6()
        # print sys.modules[__name__]
        execute_all_function()