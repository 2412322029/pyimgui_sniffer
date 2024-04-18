实时捕获界面，选择网卡处显示所有可用本机网卡，点击开始即开始捕获，下面列表显示捕获到的数据包，点击一个数据包，下方显示选中数据包的每一层信息，详细数据界面下面是日志界面，用来展示运行各个线程的日志信息，不同等级的日志用不同颜色显示。

![image](https://github.com/2412322029/pyimgui_sniffer/assets/74493337/b222f85e-d029-4dbb-8374-827938ad34d3)
实时捕获基本一致，不同的是读取的离线文件，点击目录上的统计可以显示统计IP来源
![image](https://github.com/2412322029/pyimgui_sniffer/assets/74493337/0dcb578e-95ef-467b-833e-ce60c9f438cd)


# 开发
# pyimgui_sniffer
需要安装 tshark（打包文件已包含）,路径填写到config.toml

## 安装imgui
If none of these wheels work in your environment you can install the imgui package by compiling it directly from sdist
 distribution using one of following commands:
> will install Cython as extra dependency and compile from Cython sources

`pip install imgui[Cython] --no-binary imgui`

> will compile from pre-generated C++ sources

`pip install imgui --no-binary imgui`

Microsoft Visual C++ 14.0 or greater is required. 
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

pip install -r requirement.txt

# 相关库
PyImGui库：PyImGui是一个Python绑定到C++ ImGui库的项目，而imgui是一个轻量级的图形用户界面库，ImGui的核心理念是“所见即所得”的UI设计，适用于创建简单而高效的用户界面。它提供了直观的界面元素和交互方式，用户可以方便地与流量包分析软件进行交互和操作。
scapy库：Scapy是一个基于Python编写的交互式数据包处理程序，使用Python解释器作为命令面板。可以用来发送、嗅探、解析和伪造网络数据包，常常被用于网络攻击和测试。Scapy可以实现扫描、路由跟踪、探测、单元测试、攻击和发现网络等传统功能。
pyshark库：pyshark是一个基于Tshark的Python库，用于解析和分析pcap文件。Pyshark是tshark的python包装，也就是说其底层是调用tshark实现功能，使用它从pcap文件中读取和处理数据包转换成python对象，并进行进一步的处理和分析。
