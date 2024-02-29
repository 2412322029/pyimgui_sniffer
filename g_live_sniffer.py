import os
import re
import shutil
import sys
import threading
from datetime import datetime
from tkinter import filedialog
import imgui
from shark.live_sniffer import packet_sniffer
from shark.data import MAX_SHOW, Share_Data
from util.logger import logger


def g_live_sniffer(m: imgui, share_data: Share_Data, consola_font):
    items = [i.name for i in share_data.interface_list]
    if len(items) == 0:
        logger.error('interface_list is empty 无法获取网卡设备，管理员权限打开')
        sys.exit(0)
    interface_list = share_data.interface_list
    pak_list = share_data.pak_list

    def display_packet(packet):
        imgui.push_font(consola_font)
        for lay in packet["display_packet"]:
            if imgui.tree_node(lay[0]):
                _, _ = imgui.input_text_multiline(
                    'layer', re.compile(r'\033\[[0-9;]+m').sub('', lay[1]), -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.tree_pop()
        imgui.pop_font()

    def do_save():
        if not share_data.pak_list:
            return
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pcapng",
                filetypes=[("pcapng", "*.pcapng"), ("All Files", "*.*")],
                title="Save File"
            )
            if file_path:
                shutil.move(share_data.temp, file_path)
                logger.error(f"File moved from {share_data.temp} to {file_path}")
        except FileNotFoundError:
            logger.error(f"File not found: {share_data.temp}")
        except PermissionError:
            logger.error(f"Permission error. Unable to move file.")
        pass

    flags = imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE
    m.set_next_window_size(*share_data.windows_size)
    with m.begin("实时捕获", flags=flags):
        m.text("选择网卡: ")
        m.same_line()
        imgui.set_next_item_width(500)
        if share_data.selected >= len(items) or share_data.selected < 0:
            share_data.selected = 0
        with m.begin_combo("", items[share_data.selected]) as combo:
            if combo.opened:
                for i, item in enumerate(items):
                    is_selected = (i == share_data.selected)
                    if imgui.selectable(item, is_selected)[0]:
                        share_data.selected = i
                        if share_data.pak_list:
                            share_data.dialog.save_dialog_opened = True
                            logger.debug("save?")
                            share_data.pak_list = []
                    if is_selected:
                        imgui.set_item_default_focus()

        def until_stop():
            share_data.stop[0] = True  # 存在之前的线程,设置停止标志
            while True:
                if not share_data.sniff_thread or not share_data.sniff_thread.is_alive():  # 直到停止后还原标志
                    share_data.stop[0] = False
                    break

        m.same_line()
        if m.button("开始"):
            if not share_data.sniff_thread or not share_data.sniff_thread.is_alive():  # 不存在sniff线程
                logger.debug(interface_list[share_data.selected])
                share_data.sniff_thread = threading.Thread(target=packet_sniffer,
                                                           args=(interface_list[share_data.selected].name,
                                                                 pak_list, share_data.stop,
                                                                 share_data))
                share_data.sniff_thread.start()
            else:
                until_stop()
        m.same_line()
        if m.button("停止"):
            until_stop()
        m.same_line()
        if share_data.dialog.save_dialog_opened:
            share_data.dialog.show("保存文件", do_save)
        if m.button("保存"):
            share_data.dialog.save_dialog_opened = True
        m.same_line()
        _, share_data.setting["auto_scroll"] = m.checkbox("Auto Scroll", share_data.setting["auto_scroll"])
        m.same_line()
        m.text(str(m.get_window_size()))
        m.same_line()
        if m.button("重置位置"):
            m.set_window_position(0, 32)
        table_head = ["id", "sniff_time", "src ip/mac", "dst ip/mac", "length", "protocol", "summary"]
        flag_table = imgui.TABLE_RESIZABLE | imgui.TABLE_REORDERABLE | imgui.TABLE_HIDEABLE | \
                     imgui.TABLE_BORDERS | imgui.TABLE_CONTEXT_MENU_IN_BODY | \
                     imgui.TABLE_SCROLL_X | imgui.TABLE_SCROLL_Y | imgui.TABLE_ROW_BACKGROUND
        with m.begin_child("TableScroll", 0, 500):
            with m.begin_table("t", len(table_head), flags=flag_table, outer_size_width=share_data.windows_size[0] - 10,
                               outer_size_height=500, inner_width=2520):
                m.table_setup_scroll_freeze(1, 1)
                for i in range(len(table_head)):
                    m.table_setup_column(table_head[i])
                m.table_headers_row()
                for i, row in enumerate(pak_list):
                    m.table_next_row()
                    m.table_set_column_index(0)
                    m.text(f"{i}")
                    seconds, _ = map(int, row['sniff_timestamp'].split('.'))
                    timestamp = datetime.fromtimestamp(seconds)
                    m.table_set_column_index(1)
                    m.text(f'{timestamp.strftime("%m-%d %H:%M:%S")}')
                    m.table_set_column_index(2)
                    m.text(row["src"])
                    m.table_set_column_index(3)
                    m.text(row["dst"])
                    m.table_set_column_index(4)
                    m.text(str(row["length"]))
                    m.table_set_column_index(5)
                    m.text(f"{row['highest_layer']}")
                    m.table_set_column_index(6)
                    m.text(f"{row['sport']}->{row['dport']}")
                    m.same_line()
                    m.selectable(f"##Row{i}",
                                 selected=share_data.selected_row == row,
                                 flags=imgui.SELECTABLE_ALLOW_ITEM_OVERLAP | imgui.SELECTABLE_SPAN_ALL_COLUMNS)
                    if m.is_item_clicked(0):
                        share_data.selected_row = row
                if share_data.setting["auto_scroll"]:
                    m.set_scroll_here_y(1.0)

        with m.begin_child("Scroll", 0, 400, border=True):
            if share_data.selected_row:
                display_packet(share_data.selected_row)

        m.text(f'{len(pak_list)}/{MAX_SHOW}')
        m.text("stop=" + str(share_data.stop[0]))
        m.text(f'auto_scroll:{share_data.setting["auto_scroll"]}')
        if x := share_data.selected_row:
            m.text(f"selected_row:{x['packet_count']}")
