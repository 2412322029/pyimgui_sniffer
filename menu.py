import imgui

from g_live_sniffer import g_live_sniffer
from g_show_pcap import g_show_pcap
from g_statistics import g_statistics


def menu(share_data, consola_font):
    with imgui.begin_main_menu_bar() as main_menu_bar:
        if main_menu_bar.opened:
            for i, m in enumerate(share_data.show_view):
                o = share_data.show_view[i]
                is_selected = imgui.menu_item(o[0], f'{i}', o[1], True)[0]
                if is_selected:
                    share_data.show_view[i][1] = not o[1]
                if imgui.begin_popup_context_item(f'Context{i}'):
                    imgui.menu_item("Close")
                    imgui.end_popup()

    if share_data.show_view[0][1]:
        imgui.show_demo_window()
    if share_data.show_view[1][1]:
        g_live_sniffer(imgui, share_data, consola_font)
    if share_data.show_view[2][1]:
        g_show_pcap(imgui, share_data, consola_font)
    if share_data.show_view[3][1]:
        g_statistics(imgui, share_data, consola_font)