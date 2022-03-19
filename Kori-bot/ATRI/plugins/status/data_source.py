import time
import psutil
from datetime import datetime

from ATRI.service import Service
from ATRI.log import logger as log
from ATRI.rule import is_in_service
from ATRI.exceptions import GetStatusError


__doc__ = "检查咱自身状态"


class IsSurvive(Service):
    def __init__(self):
        Service.__init__(self, "状态", __doc__, rule=is_in_service("状态"))

    @staticmethod
    def ping() -> str:
        return "I'm fine."

    @staticmethod
    def get_status():
        log.info("开始检查资源消耗...")
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            inteSENT = psutil.net_io_counters().bytes_sent / 1000000  # type: ignore
            inteRECV = psutil.net_io_counters().bytes_recv / 1000000  # type: ignore

            now = time.time()
            boot = psutil.boot_time()
            up_time = str(
                datetime.utcfromtimestamp(now).replace(microsecond=0)
                - datetime.utcfromtimestamp(boot).replace(microsecond=0)
            )
        except GetStatusError:
            raise GetStatusError("Failed to get status.")

        msg = "アトリは、高性能ですから！"
        if cpu > 90:  # type: ignore
            msg = "咱感觉有些头晕..."
            is_ok = False
            if mem > 90:
                msg = "咱感觉有点头晕并且有点累..."
                is_ok = False
        elif mem > 90:
            msg = "咱感觉有点累..."
            is_ok = False
        elif disk > 90:
            msg = "咱感觉身体要被塞满了..."
            is_ok = False
        else:
            log.info("资源占用正常")
            is_ok = True

        msg0 = (
            "Self status:\n"
            f"* CPU: {cpu}%\n"
            f"* MEM: {mem}%\n"
            f"* DISK: {disk}%\n"
            f"* netSENT: {inteSENT}MB\n"
            f"* netRECV: {inteRECV}MB\n"
            f"* Runtime: {up_time}\n"
        ) + msg

        return msg0, is_ok
