import asyncio
import tomllib
import imgui
import toml
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether
from util.ask_for_save import ask_for_save
from util.logger import logger

MAX_SHOW = 5000


class Share_Data:
    def __init__(self):
        self.stop_file_per = False
        self.windows_size = [2560, 1440]
        self.windows_pos = [0, 50]
        self.font_size = 30
        self.packet_count = 0
        # sniff
        self.tshark_path = ""
        self.interface_list = get_working_ifaces()
        self.selected: int = 0
        self.stop = [False]
        self.sniff_thread = None
        self.file_per_thread = None
        self.pak_list = []
        self.selected_row = None
        # show pcap
        self.temp = tempfile.mktemp()
        self.file_pak_list = []
        self.file_path = None
        self.file_loading = False
        self.file_total = 0
        self.selected_file_row = None

        self.loop = asyncio.new_event_loop()
        self.dialog = ask_for_save()
        self.theme = "light"
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
        logger.debug('init end')

    def get_file_capture(self, path):
        def file_capture(p):
            self.file_loading = True
            logger.debug(f"open: {p}")
            try:
                if self.loop.is_closed():
                    self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                plist = rdpcap(p)
                self.file_total = len(plist)
                for i in plist:
                    if not self.stop_file_per:
                        self.file_pak_list.append(Share_Data.per_file_pak(i))
                    else:
                        break
                self.file_loading = False
                self.loop.stop()
                self.loop.close()
            except Exception:
                logger.error(f"Exception in thread {threading.current_thread().name}", exc_info=True)

        self.file_per_thread = threading.Thread(target=file_capture, args=(path,))
        self.file_per_thread.start()

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
        logger.info("save config")

    def load_config(self):
        config_data = tomllib.load(open("config.toml", "rb"))
        for key, value in config_data.items():
            setattr(self, key, value)
        logger.info("load config")

    def before_close(self):
        logger.debug("before close window, stop thread [start]")
        self.stop[0] = True  # 存在之前的线程,设置停止标志
        self.stop_file_per = True
        if self.sniff_thread:
            while True:
                if not self.sniff_thread.is_alive():  # 直到停止后还原标志
                    self.stop[0] = False
                    break
        if self.file_per_thread:
            while True:
                if not self.file_per_thread.is_alive():
                    self.stop_file_per = False
                    break
        logger.debug("before close window, stop sniff thread [end]")
        if os.path.isfile(self.temp):
            os.remove(self.temp)
            logger.debug(f"remove temp file from {self.temp}")
        self.save_config()

    def set_style(self):
        if self.theme == "light":
            imgui.style_colors_light()
        elif self.theme == "dark":
            imgui.style_colors_dark()
        elif self.theme == "classic":
            imgui.style_colors_classic()

    @staticmethod
    def per_file_pak(pkt: Packet):
        try:
            pkt.packet_count = 0
        except AttributeError:
            pass
        src = ""
        dst = ""
        sport = ""
        dport = ""
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
        elif Ether in pkt:
            src = pkt[Ether].src
            dst = pkt[Ether].dst

        if TCP in pkt:
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
        elif UDP in pkt:
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
        return {
            "sniff_timestamp": pkt.time,
            "src": src,
            "dst": dst,
            "sport": sport,
            "dport": dport,
            "length": len(pkt),
            "highest_layer": pkt.lastlayer(),
            "summary": pkt.summary(),
            "full": pkt
        }

    @staticmethod
    def per_pak(pak):  # 包装解析的pak,避免重复解析数据
        try:
            pak.packet_count = 0
        except AttributeError:
            pass
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
            "packet_count": pak.packet_count,
            # "full": pak,
            "display_packet": [(lay.layer_name, str(lay)) for lay in pak.layers]
        }


if __name__ == '__main__':
    s = Share_Data()
    s.load_config()
    print(vars(s))
