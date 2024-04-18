from scapy.all import *

used_iface_name = "WLAN 2"


if __name__ == '__main__':
    for i in get_working_ifaces():
        print(f"{i}  {i.name}  {i.description} {i.ip} {i.mac}")
