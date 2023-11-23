import asyncio
import os
import tomllib

import imgui
from scapy.all import get_working_ifaces
import tempfile
from util.ask_for_save import ask_for_save
import pyshark
import toml

MAX_SHOW = 5000


class Share_Data:
    def __init__(self):
        self.windows_size = [2560, 1440]
        self.temp = tempfile.mktemp()
        self.windows_pos = [0, 50]
        self.font_size = 30
        self.packet_count = 0
        self.interface_list = get_working_ifaces()
        self.selected: int = 0
        self.stop = [False]
        self.sniff_thread = None
        self.pak_list = []
        self.file_pak_list = []
        self.file_opened = False
        self.selected_row = None
        self.loop = asyncio.new_event_loop()
        self.dialog = ask_for_save()
        self.theme = "light"
        self.tshark_path = ""
        self.setting = {
            "auto_scroll": True
        }
        self.show_view = [
            ['Demo', False],
            ['实时捕获', False],
            ['show pcap', False]
        ]
        self.load_config()
        self.set_style()
        print('init end')

    def get_file_capture(self, path):
        print(f"open: {path}")
        pak_list = pyshark.FileCapture(input_file=path, tshark_path=self.tshark_path)
        for i in pak_list:
            self.file_pak_list.append(Share_Data.per_file_pak(i))

    def save_config(self):
        config_data = {
            "font_size": self.font_size,
            "show_view": self.show_view,
            "windows_pos": self.windows_pos,
            "windows_size": self.windows_size,
            "setting": self.setting,
            "selected": self.selected,
            "theme": self.theme,
            "tshark_path": self.tshark_path
        }
        with open("config.toml", "w", encoding="utf8") as f:
            toml.dump(config_data, f)
        print("save config")

    def load_config(self):
        config_data = tomllib.load(open("config.toml", "rb"))
        for key, value in config_data.items():
            setattr(self, key, value)
        print("load config")

    def before_close(self):
        if self.sniff_thread:
            print("before close window, stop sniff thread [start]")
            self.stop[0] = True  # 存在之前的线程,设置停止标志
            while True:
                if not self.sniff_thread.is_alive():  # 直到停止后还原标志
                    self.stop[0] = False
                    break
            print("before close window, stop sniff thread [end]")
        if os.path.isfile(self.temp):
            os.remove(self.temp)
            print("remove temp file")
        self.save_config()

    def set_style(self):
        if self.theme == "light":
            imgui.style_colors_light()
        elif self.theme == "dark":
            imgui.style_colors_dark()
        elif self.theme == "classic":
            imgui.style_colors_classic()

    @staticmethod
    def per_file_pak(pak):  # 包装解析的pak,避免重复解析数据
        sport = ""
        dport = ""
        if "IP" in pak:
            src = f'{pak.ip.src}'
            dst = f'{pak.ip.dst}'
        else:
            src = f'{pak.eth.src}'
            dst = f'{pak.eth.dst}'
        if "TCP" in pak:
            sport = pak.tcp.srcport
            dport = pak.tcp.dstport
        elif "UDP" in pak:
            sport = pak.udp.srcport
            dport = pak.udp.dstport
        return {
            "number": pak.number,
            "sniff_timestamp": pak.sniff_timestamp,
            "src": src,
            "dst": dst,
            "sport": sport,
            "dport": dport,
            "length": pak.length,
            "highest_layer": pak.highest_layer,
            # "full": pak,
            "display_packet": [(lay.layer_name, str(lay)) for lay in pak.layers]
        }


if __name__ == '__main__':
    s = Share_Data()
    s.load_config()
    print(vars(s))
