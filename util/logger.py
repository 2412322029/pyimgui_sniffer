import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler

FORMAT = "[%(asctime)-15s] [%(threadName)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger("main")
if not os.path.exists("log"):
    os.makedirs("log")
handler = TimedRotatingFileHandler("log/sniffer.log", when="midnight", interval=1, backupCount=10, encoding="utf-8")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
# when=midnight时,suffix、extMatch默认值为
handler.suffix = "%Y-%m-%d"
extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
handler.extMatch = re.compile(extMatch, re.ASCII)

handler.setFormatter(formatter)
logger.addHandler(handler)
