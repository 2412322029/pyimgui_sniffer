
from util.logger import log_stream

# 定义日志级别的颜色映射
level_colors = {
    "DEBUG": (0.5, 0.5, 0.5),  # 灰色
    "INFO": (0.36, 0.64, 0.977),  # 蓝色
    "WARNING": (1.0, 1.0, 0.0,),  # 黄色
    "ERROR": (1.0, 0.0, 0.0)  # 红色
}


def show_log(m, share_data):
    with m.begin_child("日志", 0, 200, border=True, flags=m.WINDOW_HORIZONTAL_SCROLLING_BAR):
        # 获取当前日志内容
        log_lines = log_stream.getvalue().splitlines()[-1000:]
        # 只显示最多1000行日志
        last_color = None
        for line in log_lines:
            matched = False
            for level, color in level_colors.items():
                if f"[{level}]" in line:
                    m.text_colored(line, *color)
                    last_color = color
                    matched = True
                    break
            if not matched:
                # 如果没有匹配到任何级别，则显示上一种颜色
                m.text_colored(line, *last_color)
        # 将"清空日志"按钮放在同一行并靠右显示
        m.set_cursor_pos_x(m.get_cursor_pos_x() + m.get_column_width() - 100 - m.get_scroll_x() - 2 * m.get_style().item_spacing.x);
        # m.same_line()
        if m.button("清空日志"):
            log_stream.truncate(0)
        if len(log_lines) >= 2:
            if share_data.log_new_line != log_lines[-1]:
                m.set_scroll_y(m.get_scroll_max_y())
                # print("aa")
            share_data.log_new_line = log_lines[-1]
