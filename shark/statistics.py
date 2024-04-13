from collections import Counter
from scapy.plist import PacketList

from util.load_img import img_list, load_img
from util.logger import logger
import matplotlib.pyplot as plt
import matplotlib
from util.run_with import run_once, run_in_thread

matplotlib.use('Agg')


@run_once
@run_in_thread
def statistics(pcap_file, result_image_path):
    # 检查pcap_file是否为PacketList类型
    if not isinstance(pcap_file, PacketList):
        logger.error("pcap_file不是PacketList类型")
        return

    # 统计不同协议类型的数据包数量
    protocol_counts = Counter(packet.lastlayer().name for packet in pcap_file)

    # 提取协议类型和对应的数量
    protocols = list(protocol_counts.keys())
    counts = list(protocol_counts.values())

    # 创建饼图
    plt.pie(counts, labels=protocols, autopct='%1.1f%%')
    plt.title("Protocol Distribution")
    plt.savefig(result_image_path)
    # img_list.pop(result_image_path)

    logger.info(f"plt save {result_image_path}")
