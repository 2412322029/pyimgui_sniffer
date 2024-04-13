from pprint import pprint
from tkinter import filedialog
import imgui
from shark.data import Share_Data
from util.logger import logger, log_stream
from util.show_log import show_log


def g_show_pcap(m: imgui, share_data: Share_Data, consola_font):
    def display_packet(packet):
        imgui.push_font(consola_font)
        for lay in packet["full"].layers():
            if imgui.tree_node(str(lay.name)):
                content = ""
                for field in lay.fields_desc:
                    field_name = field.name
                    field_value = getattr(lay, field_name)
                    content += f"{field_name}: {field_value}\n"
                _, _ = imgui.input_text_multiline('layer', content, -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.tree_pop()
        imgui.pop_font()

    def reload():
        share_data.file_pak_list = []
        share_data.get_file_capture(share_data.file_path)
        share_data.file_pagenum = 0

    flags = imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
    m.set_next_window_size(*share_data.windows_size)
    with m.begin("show pcap", flags=flags):
        if not share_data.file_loading:
            if m.button("打开文件"):
                share_data.file_pagenum = 0
                share_data.file_path = filedialog.askopenfilename(
                    defaultextension=".pcapng",
                    filetypes=[("pcapng", "*.pcapng"), ("All Files", "*.*")],
                    title="Open File"
                )
                if share_data.file_path:
                    share_data.file_pak_list = []
                    share_data.get_file_capture(share_data.file_path)
            m.same_line()
            if m.button("清除"):
                logger.debug("clear file_pak_list")
                share_data.file_pak_list = []
                share_data.file_path = None
                share_data.file_per_thread = None
            if share_data.file_path:
                m.same_line()
                if m.button("重新加载"):
                    reload()
                m.same_line()
                m.text(share_data.file_path)
                # m.same_line()
                m.push_item_width(200)
                m.same_line(m.get_window_width() - m.calc_text_size(
                    "page").x - m.get_style().item_spacing.x)
                m.set_cursor_pos_x(m.get_cursor_pos_x() - m.get_style().item_spacing.x - 200)
                ch, p = m.input_int("", share_data.file_pagenum)
                if ch and 0 <= p < len(share_data.file_pak_list) / share_data.file_pagesize:
                    share_data.file_pagenum = p
                m.pop_item_width()

        else:
            m.text(f"loading...")
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
                for i, row in enumerate(share_data.file_pak_list
                                        [share_data.file_pagenum * share_data.file_pagesize:
                                        (share_data.file_pagenum + 1) * share_data.file_pagesize]):
                    m.table_next_row()
                    m.table_set_column_index(0)
                    m.text(f'{i + share_data.file_pagesize * share_data.file_pagenum}')
                    m.table_set_column_index(1)
                    m.text(f'{str(row["sniff_timestamp"])}')
                    m.table_set_column_index(2)
                    m.text(row["src"])
                    m.table_set_column_index(3)
                    m.text(row["dst"])
                    m.table_set_column_index(4)
                    m.text(str(row["length"]))
                    m.table_set_column_index(5)
                    m.text(f"{row['highest_layer']}")
                    m.table_set_column_index(6)
                    m.text(f"{row['sport']}->{row['dport'], row['summary']}")
                    m.same_line()
                    m.selectable(f"##Row{i}", selected=share_data.selected_file_row == row,
                                 flags=imgui.SELECTABLE_ALLOW_ITEM_OVERLAP | imgui.SELECTABLE_SPAN_ALL_COLUMNS)
                    if m.is_item_clicked(0):
                        share_data.selected_file_row = row

                        # print(f"Clicked on row {i}")
                if share_data.setting["auto_scroll"]:
                    m.set_scroll_here_y(1.0)
                # sort_specs = m.table_get_sort_specs()
                # if sort_specs:
                #     if sort_specs.specs_dirty:
                #         sort_specs.specs_dirty = False
                #         share_data.file_pak_list.sort(key=lambda item: str(item))
                #         print(sort_specs)
        with m.begin_child("Scroll_table", 0, 400, border=True):
            if share_data.selected_file_row:
                display_packet(share_data.selected_file_row)

        show_log(m, share_data)
        with m.begin_child("状态", 0, 30):
            m.text(f'{len(share_data.file_pak_list)}')
            m.same_line()
            m.text("stop=" + str(share_data.stop[0]))
            m.same_line()
            m.text(f'auto_scroll:{share_data.setting["auto_scroll"]}')
