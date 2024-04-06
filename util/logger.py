import logging
import os
import io
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

# 创建一个内存缓冲区作为日志输出目标
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
log_stream = io.StringIO()
log_stream.truncate(MAX_LOG_SIZE)
handler = logging.StreamHandler(log_stream)

handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)
