# TCP client
import socket
import logging
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
port = 10000
adresa = '198.7.0.2'
server_address = (adresa, port)

def send_message_from_client(mesaj):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    logging.info('Handshake cu %s', str(server_address))
    sock.connect(server_address)
    time.sleep(3)
    sock.send(mesaj.encode('utf-8'))
    data = sock.recv(1024)
    logging.info('Content primit: "%s"', data)
    sock.close()    

# def close_connection():
#     global sock
#     logging.info('closing socket')
#     sock.close()
