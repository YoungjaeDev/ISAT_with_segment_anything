# -*- coding: utf-8 -*-

"""Check that the GPU monitor thread stops on request instead of blocking forever.

Runs headless. Works with or without an nvidia GPU: without one the polling
body falls into its except branch, which is still enough to exercise the loop
and the stop flag. Run directly:

    uv run python test/gpu_resource_thread_stop.py
"""

import os
import sys
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QCoreApplication

from ISAT.segment_any.gpu_resource import GPUResource_Thread

JOIN_TIMEOUT_MS = 5000


def main():
    app = QCoreApplication.instance() or QCoreApplication(sys.argv)

    thread = GPUResource_Thread()
    thread.start()

    # 루프가 최소 한 바퀴는 돌게 둔다
    time.sleep(0.3)
    assert thread.isRunning(), "스레드가 시작되지 않았다"

    started = time.monotonic()
    thread.stop()
    joined = thread.wait(JOIN_TIMEOUT_MS)
    elapsed = time.monotonic() - started

    assert joined, (
        f"stop() 후 {JOIN_TIMEOUT_MS}ms 안에 스레드가 끝나지 않았다 (무한 루프)"
    )
    assert thread.isFinished(), "스레드가 종료 상태가 아니다"
    print(f"GPU monitor thread stopped in {elapsed:.2f}s")

    del app


if __name__ == "__main__":
    main()
