from collections import Counter

from scapy.all import *
from scapy.layers.inet import IP

# 加载 pcap 文件
packets = rdpcap('D:\\24123\\code\\py\\pyimgui_sniffer\\output\\2.pcapng')

for p in packets:
    if p.haslayer('ARP'):
        p.show()
