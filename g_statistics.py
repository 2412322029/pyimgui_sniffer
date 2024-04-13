import os

import imgui

from shark.data import Share_Data
from shark.statistics import statistics
from util.load_img import load_img


def g_statistics(m: imgui, share_data: Share_Data, consola_font):
    flags = imgui.WINDOW_NO_COLLAPSE
    with (m.begin("统计", flags=flags)):
        if share_data.file_path and share_data.pcap_file:
            m.text(share_data.file_path)
            m.text(share_data.pcap_file.__str__())
            statistics(share_data.pcap_file, share_data.result_image_path)
        if m.button("show"):
            load_img(share_data.result_image_path, 1)

