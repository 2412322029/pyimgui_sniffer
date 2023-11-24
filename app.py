import subprocess
import sys


def hide_console(file):
    if sys.platform.startswith('win'):
        subprocess.Popen([sys.executable, file], creationflags=subprocess.CREATE_NO_WINDOW, close_fds=True)
    else:
        subprocess.Popen([sys.executable, file])


if __name__ == "__main__":
    hide_console('main.py')
