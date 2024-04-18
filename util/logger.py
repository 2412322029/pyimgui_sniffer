import logging
import os
import io
import re
from logging.handlers import TimedRotatingFileHandler

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
log_stream = io.StringIO()
# 创建一个内存缓冲区作为日志输出目标

FORMAT = "%(asctime)-15s [%(threadName)s] [%(levelname)s] [%(pathname)s:%(lineno)d] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger("main")
if not os.path.exists("log"):
    os.makedirs("log")

# 创建内存日志处理程序
log_stream_handler = logging.StreamHandler(log_stream)
log_stream_handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(log_stream_handler)

# 创建文件日志处理程序
file_handler = TimedRotatingFileHandler("log/sniffer.log", when="midnight", interval=1, backupCount=10, encoding="utf-8")
file_handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(file_handler)
