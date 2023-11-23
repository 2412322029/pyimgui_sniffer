from pprint import pprint

import pyshark

def get_cap(path):
    cap = pyshark.FileCapture(input_file=path, tshark_path="D:\\soft\\Wireshark\\tshark.exe")
    return cap
# 遍历所有的数据包
# for packet in cap:
#     src = packet.eth.src
#     dst = packet.eth.dst
#     protocol = packet.transport_layer
#     print(f"Packet: {protocol} from {src} to {dst}")