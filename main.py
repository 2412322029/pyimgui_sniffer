#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from OpenGL.GL import *
import glfw
import sys
from menu import menu
from shark import data
from util.logger import logger
import imgui
from imgui.integrations.glfw import GlfwRenderer

main_directory = os.path.dirname(os.path.abspath(__file__))


def main():
    imgui.create_context()
    share_data = data.Share_Data(main_directory)
    window = impl_glfw_init(share_data)
    glfw.set_window_pos(window, *share_data.windows_pos)
    impl = GlfwRenderer(window)
    io = imgui.get_io()
    chinese_font = io.fonts.add_font_from_file_ttf("c:/Windows/Fonts/msyh.ttc",
                                                   share_data.font_size, None,
                                                   io.fonts.get_glyph_ranges_chinese())
    consola_font = io.fonts.add_font_from_file_ttf("./font/consola.ttf",
                                                   share_data.font_size, None)
    impl.refresh_font_texture()
    while not glfw.window_should_close(window):
        def on_window_size_change(_, width, height):
            share_data.windows_size[0], share_data.windows_size[1] = width, height

        def on_window_pos_change(_, x, y):
            share_data.windows_pos[0], share_data.windows_pos[1] = x, y

        glfw.set_window_size_callback(window, on_window_size_change)
        glfw.set_window_pos_callback(window, on_window_pos_change)
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        glfw.swap_interval(1)
        imgui.push_font(chinese_font)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, 0.57, 0.76, 0.98, 0.40)
        if not glfw.get_window_attrib(window, glfw.ICONIFIED):
            menu(share_data, consola_font)  # 菜单
        imgui.pop_font()
        imgui.pop_style_color()

        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    share_data.before_close()
    impl.shutdown()
    glfw.terminate()


def impl_glfw_init(share_data):
    width, height = share_data.windows_size
    window_name = "PyImGui Sniffer"

    if not glfw.init():
        logger.error("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        logger.error("Could not initialize Window")
        sys.exit(1)

    return window


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.error(f"An unhandled exception occurred", exc_info=True)
    except KeyboardInterrupt as e:
        logger.error(f"Ctrl c by user")
