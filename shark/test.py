import matplotlib
from scapy.all import *
import matplotlib.pyplot as plt

# 加载 pcap 文件
packets = rdpcap('D:\\24123\\code\\py\\pyimgui_sniffer\\output\\2.pcapng')


# 定义一个函数，返回标签和值的元组
def get_label_value(packet):
    label = "Packet Size"
    value = len(packet)
    return label, value


# 调用 multiplot() 方法并获取返回的 Line2D 对象列表
lines = packets.multiplot(get_label_value)
print(lines)
# 创建一个新的 Matplotlib 图形对象
fig, ax = plt.subplots()

# 将 Line2D 对象列表中的每个线条逐个添加到图形中
for line in lines:
    for l in line:
        ax.add_line(l)

# 设置图形的标题、轴标签等
ax.set_title("Packet Size Distribution")
ax.set_xlabel("Packet Index")
ax.set_ylabel("Packet Size")

# 显示图形
plt.show()
