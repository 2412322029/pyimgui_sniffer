import imgui

from shark.data import Share_Data


def g_statistics(m: imgui, share_data: Share_Data, consola_font):
    # flags = imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE
    m.set_next_window_size(*share_data.windows_size)
    with m.begin("统计"):
        m.text("")
