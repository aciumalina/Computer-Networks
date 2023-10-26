# TCP Server
import socket
import logging
import time
from socket import error as SocketError

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2'
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
sock.listen(5)
while True:
    try:
        logging.info('Asteptam conexiuni...')
        conexiune, address = sock.accept()
        logging.info("Handshake cu %s", address)
        time.sleep(2)
        data = conexiune.recv(1024)
        logging.info('Content primit: "%s"', data)
        conexiune.send(b"Server a primit mesajul: " + data)
        conexiune.close()
    except SocketError as e:
        conexiune.close()
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        sock.bind(server_address)
    except KeyboardInterrupt:
        conexiune.close()
        sock.close()
        logging.info("Conexiune inchisa")
        break

    
