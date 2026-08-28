# -*- coding: utf-8 -*-
# @Author  : LG

import os
import platform

from PyQt5.QtCore import QThread, pyqtSignal

osplatform = platform.system()


class GPUResource_Thread(QThread):
    """
    The thread for monitoring GPU0 resources.

    Arguments:
        gpu_id (int): The id of the GPU device to monitor. default 0.
    """

    message = pyqtSignal(str)

    # nvidia-smi 를 매 반복 띄우므로 간격을 두지 않으면 CPU 를 그대로 먹는다
    POLL_INTERVAL_MS = 1000

    def __init__(self, gpu_id: int = 0):
        super(GPUResource_Thread, self).__init__()
        self.gpu_id = gpu_id
        self._running = True

        if osplatform == "Windows":
            self.command = "nvidia-smi -q -d MEMORY -i {} | findstr".format(self.gpu_id)
        elif osplatform == "Linux":
            self.command = "nvidia-smi -q -d MEMORY -i {} | grep".format(self.gpu_id)
        elif osplatform == "Darwin":
            self.command = "nvidia-smi -q -d MEMORY -i {} | grep".format(self.gpu_id)
        else:
            self.command = "nvidia-smi -q -d MEMORY -i {} | grep".format(self.gpu_id)
        try:
            r = os.popen("{} Total".format(self.command)).readline()
            self.total = r.split(":")[-1].strip().split(" ")[0]
        except Exception as e:
            print(e)
            self.total = "none"

    def run(self):
        while self._running:
            try:
                r = os.popen("{} Used".format(self.command)).readline()
                used = r.split(":")[-1].strip().split(" ")[0]
                self.message.emit("cuda: {}/{}MiB".format(used, self.total))
            except:
                self.message.emit("cuda: {}/{}MiB".format("-", "-"))
            self.msleep(self.POLL_INTERVAL_MS)

    def stop(self):
        """Ask the polling loop to finish. Call wait() afterwards to join."""
        self._running = False

    def __del__(self):
        # 플래그를 내리지 않으면 wait() 가 영원히 돌아오지 않는다
        self._running = False
        try:
            self.wait()
        except RuntimeError:
            # PyQt 가 C++ 객체를 먼저 지운 뒤에 __del__ 이 도는 경우
            pass
