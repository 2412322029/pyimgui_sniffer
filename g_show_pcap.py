import re
from datetime import datetime
import imgui
from shark.data import MAX_SHOW, Share_Data
from tkinter import filedialog


def g_show_pcap(m: imgui, share_data: Share_Data, consola_font):
    def display_packet(packet):
        imgui.push_font(consola_font)
        for lay in packet["display_packet"]:
            if imgui.tree_node(lay[0]):
                _, _ = imgui.input_text_multiline(
                    'layer', re.compile(r'\033\[[0-9;]+m').sub('', lay[1]), -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.tree_pop()
        imgui.pop_font()

    flags = imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE
    m.set_next_window_size(*share_data.windows_size)
    with m.begin("show pcap", flags=flags):
        if m.button("Open"):
            file_path = filedialog.askopenfilename(
                defaultextension=".pcapng",
                filetypes=[("pcapng", "*.pcapng"), ("All Files", "*.*")],
                title="Open File"
            )
            if file_path and not share_data.file_opened:
                share_data.get_file_capture(file_path)
                share_data.file_opened = True
        m.same_line()
        if m.button("Close"):
            share_data.file_opened = False
            print("clear file_pak_list")
            share_data.file_pak_list = []
        # m.set_window_position(0, 32)
        table_head = ["id", "sniff_time", "src ip/mac", "dst ip/mac", "length", "protocol", "summary"]
        flag_table = imgui.TABLE_RESIZABLE | imgui.TABLE_REORDERABLE | imgui.TABLE_HIDEABLE | \
                     imgui.TABLE_BORDERS | imgui.TABLE_CONTEXT_MENU_IN_BODY | \
                     imgui.TABLE_SCROLL_X | imgui.TABLE_SCROLL_Y | \
                     imgui.TABLE_SORT_MULTI | imgui.TABLE_SORTABLE | imgui.TABLE_ROW_BACKGROUND
        with m.begin_child("TableScroll_show", 0, 500):
            with m.begin_table("t_show", len(table_head), flags=flag_table,
                               outer_size_width=share_data.windows_size[0] - 10,
                               outer_size_height=500, inner_width=2520):
                m.table_setup_scroll_freeze(1, 1)
                for i in range(len(table_head)):
                    m.table_setup_column(table_head[i])
                m.table_headers_row()
                for i, row in enumerate(share_data.file_pak_list, start=1):
                    m.table_next_row()
                    m.table_set_column_index(0)
                    m.text(f'{i}')
                    seconds, _ = map(int, row["sniff_timestamp"].split('.'))
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
                    m.selectable(f"##Row{i}", selected=share_data.selected_row == row,
                                 flags=imgui.SELECTABLE_ALLOW_ITEM_OVERLAP | imgui.SELECTABLE_SPAN_ALL_COLUMNS)
                    if m.is_item_clicked(0):
                        share_data.selected_row = row

                        print(f"Clicked on row {i}")
                if share_data.setting["auto_scroll"]:
                    m.set_scroll_here_y(1.0)
                # sort_specs = m.table_get_sort_specs()
                # if sort_specs:
                #     if sort_specs.specs_dirty:
                #         sort_specs.specs_dirty = False
                #         share_data.file_pak_list.sort(key=lambda item: str(item))
                #         print(sort_specs)
        with m.begin_child("Scroll_table", 0, 400, border=True):
            if share_data.selected_row:
                display_packet(share_data.selected_row)

        m.text(f'{len(share_data.file_pak_list)}/{MAX_SHOW}')
        m.text("stop=" + str(share_data.stop[0]))
        m.text(f'auto_scroll:{share_data.setting["auto_scroll"]}')
