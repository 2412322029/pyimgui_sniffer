import atexit
import os
import tempfile
from collections import Counter

from scapy.layers.inet import IP
from scapy.plist import PacketList

from util.load_img import img_list, load_img
from util.logger import logger
import matplotlib.pyplot as plt
import matplotlib
from util.run_with import run_once, run_in_thread

matplotlib.use('Agg')


class statistics:
    img_result = {}

    def __init__(self, pcap_file):
        # 检查pcap_file是否为PacketList类型
        if not isinstance(pcap_file, PacketList):
            raise TypeError("pcap_file不是PacketList类型")
        if statistics.img_result.values():
            statistics.img_result.clear()
        self.pcap_file = pcap_file

    @run_in_thread
    def count_ip_src(self):
        result_image_path = tempfile.mktemp(suffix=".png")
        ip_src = []
        for p in self.pcap_file:
            if p.haslayer(IP):
                ip_src.append(p[IP].src)
        counter_result = Counter(ip_src)
        logger.debug(counter_result)

        categories = list(counter_result.keys())
        values = list(counter_result.values())
        bars = plt.barh(categories, values, color='skyblue')
        # 添加标题和标签
        plt.title('IP Source Count')
        plt.xlabel('Count')
        plt.ylabel('IP Source')
        plt.subplots_adjust(left=0.25)
        # 在每个条形上显示数值
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height() / 2, width, ha='left', va='center')
        plt.savefig(result_image_path)
        statistics.img_result.update({"count_ip_src": result_image_path})


@atexit.register
def clear_img():
    for f in statistics.img_result.values():
        if os.path.isfile(f):
            os.remove(f)
    logger.debug(f"remove temp file from {statistics.img_result.values()}")
    statistics.img_result.clear()
