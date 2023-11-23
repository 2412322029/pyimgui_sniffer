

import imgui


class ask_for_save:
    def __init__(self):
        self.uuid = "uuid"
        self.callback = None
        self.text = ""
        self.save_dialog_opened = False

    def show(self, text: str, callback, *args, **kwargs):
        self.callback = callback
        self.text = text
        if self.save_dialog_opened:
            imgui.open_popup("Save Dialog #" + str(self.uuid))
        if imgui.begin_popup_modal("Save Dialog #" + str(self.uuid),
                                   imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE).opened:
            imgui.text(self.text)
            if imgui.button("Yes"):
                if self.callback:
                    print("yes callback")
                    self.callback(*args, **kwargs)
                    imgui.close_current_popup()
                    self.save_dialog_opened = False
            imgui.same_line()
            if imgui.button("No"):
                imgui.close_current_popup()
                self.save_dialog_opened = False
            imgui.end_popup()
