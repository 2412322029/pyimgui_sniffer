import asyncio
import pyshark
from shark.data import Share_Data, MAX_SHOW


def packet_sniffer(name, pak_list: list, stop_flag, share_data: Share_Data):
    print("packet_sniffer starting...")
    if share_data.loop.is_closed():
        share_data.loop = asyncio.new_event_loop()
    cap = pyshark.LiveCapture(interface=name, tshark_path=share_data.tshark_path,
                              output_file=share_data.temp,
                              eventloop=share_data.loop)
    print(f'temp file path: {share_data.temp}')
    for pak in cap.sniff_continuously():
        if len(pak_list) >= MAX_SHOW:
            pak_list.remove(pak_list[0])
        share_data.packet_count += 1
        pak.packet_count = share_data.packet_count
        pak_list.append(Share_Data.per_file_pak(pak))
        # print(pak.packet_count)
        if stop_flag[0]:  # Stop the capture
            cap.close()
            share_data.loop.stop()
            share_data.loop.close()
            break
    print("packet_sniffer end... ")
