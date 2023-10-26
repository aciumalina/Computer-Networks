#Documetation
#https://abdesol.medium.com/lets-make-a-trace-routing-tool-from-scratch-with-python-f2f6f78c3c55
#https://www.freecodecamp.org/news/how-to-get-location-information-of-ip-address-using-python/


import sys
import socket
import struct
import requests

def showIpDetails(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    if response.get('reserved'):
        print(f'The current ip:{ip} -> is part of a private network')
        return

    if response.get('reason') == 'RateLimited':
        print("The API fetching the IP details sent a Rate Limited Message. Please wait a minute and try again (to reset the limit).")
        return

    if response.get('error'):
        print("Unexpected error while fetching IP's location.")
        return


    location_data = {
        "ip": ip,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    print(location_data)
def create_sending_socket():
    udp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))
    return udp_send_sock



def create_receiving_socket(timeout):
    icmp_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    # creez o structura pentru a seta timeoutul pentru socketul icmp
    timeout_struct = struct.pack('ll', timeout, 0)
    icmp_recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout_struct)
    return icmp_recv_socket

def modify_ttl_value(udp_socket, ttl):
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    return udp_socket


def receive_message(receive_socket, no_of_tries):
    addr = None
    while no_of_tries:
        try:
            _, addr = receive_socket.recvfrom(1024)
            message_received = True
        except Exception as e:
            # print(e)
            no_of_tries -= 1
            continue

        if message_received:
            return addr[0]
    return addr

def send_message(send_socket, message, target_ip, target_port):
    send_socket.sendto(message, (target_ip, target_port))

def traceroute(target_host, timeout_input, no_of_tries):

    # Obținerea adresei IP a destinației
    target_ip = socket.gethostbyname(target_host)
    target_port = 33434

    currentTimeToLive = 1

    timeout = int(timeout_input)

    # socket de UDP (senderul)
    udp_send_sock = create_sending_socket()

    # socket RAW de citire a răspunsurilor ICMP (receiverul)
    receive_socket = create_receiving_socket(timeout)

    while True:
        # setam valoarea ttl curenta
        udp_send_sock = modify_ttl_value(udp_send_sock, currentTimeToLive)

        # trimite un mesaj UDP catre un tuplu (IP, port)
        send_message(udp_send_sock, b'message', target_ip, target_port)

        ip_router = receive_message(receive_socket, int(no_of_tries))
        if ip_router is not None:
            showIpDetails(ip_router)
        else:
            print(f'The current node did not send an ICMP message')
        # inseamna ca am ajuns la nodul final

        if ip_router == target_ip:
            break
        currentTimeToLive += 1

if __name__ == '__main__':
    traceroute(sys.argv[1],sys.argv[2],sys.argv[3])