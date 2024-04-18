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
