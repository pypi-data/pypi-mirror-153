# 从性能角度来讲，windows系统使用IOCP、linux使用epoll是高并发情况下最好的实现，他们都是多路IO服用，不是并行框架
# windows IOCP可以使用twisted
# 从简单和通用角度来讲，本模块使用flask+gevent实现，
from gevent import monkey
import socket
import gevent

monkey.patch_all()

server = socket.socket()
server.bind(('0.0.0.0', 8890))
server.listen(1000)


def worker(conn):
    data = conn.recv(1024)
    if data:
        print(data.decode('utf8'))
        conn.send(data)
    else:
        conn.close()


while True:
    conn, addr = server.accept()  # 获得连接
    gevent.spawn(worker, conn)  #
