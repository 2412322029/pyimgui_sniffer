import os

import imgui

from shark.data import Share_Data
from shark.statistics import statistics, clear_img
from util.load_img import load_img


def g_statistics(m: imgui, share_data: Share_Data, consola_font):
    flags = imgui.WINDOW_NO_COLLAPSE
    with (m.begin("统计", flags=flags)):
        if share_data.file_path and share_data.pcap_file:
            m.text(share_data.file_path)
            m.text(share_data.pcap_file.__str__())
        if m.button("统计"):
            statistics(share_data.pcap_file).count_ip_src()
        if m.button("清除"):
            clear_img()
        if statistics.img_result.get("count_ip_src"):
            load_img(statistics.img_result.get("count_ip_src"), 1)
