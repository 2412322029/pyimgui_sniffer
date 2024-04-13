import asyncio
import threading

import pyshark
from shark.data import Share_Data, MAX_SHOW
from util.logger import logger


def packet_sniffer(name, pak_list: list, stop_flag, share_data: Share_Data):
    try:
        logger.debug("packet_sniffer starting...")
        if share_data.loop.is_closed():
            share_data.loop = asyncio.new_event_loop()
        cap = pyshark.LiveCapture(interface=name, tshark_path=share_data.tshark_path,
                                  output_file=share_data.temp,
                                  eventloop=share_data.loop)
        logger.debug(f'temp file path: {share_data.temp}')
        for pak in cap.sniff_continuously():
            if len(pak_list) >= MAX_SHOW:
                pak_list.remove(pak_list[0])
            share_data.packet_count += 1
            pak.packet_count = share_data.packet_count
            pak_list.append(Share_Data.per_pak(pak))
            # print(pak.packet_count)
            if stop_flag[0]:  # Stop the capture
                cap.close()
                share_data.loop.stop()
                share_data.loop.close()
                break
        logger.debug("packet_sniffer end... ")
    except Exception as e:
        logger.error(f"Exception in thread {threading.current_thread().name}:\n{e}", exc_info=True)

