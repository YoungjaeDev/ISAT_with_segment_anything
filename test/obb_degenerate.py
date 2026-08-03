# -*- coding: utf-8 -*-

"""Check that a zero-length first OBB edge does not divide by zero.

Runs headless (offscreen Qt platform). Run directly:

    uv run python test/obb_degenerate.py
"""

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5 import QtCore, QtWidgets

from ISAT.configs import SOFTWARE_CONFIG_FILE, load_config
from ISAT.widgets.canvas import AnnotationScene
from ISAT.widgets.polygon import OBB


class StubMainWindow:
    """Minimal stand-in for MainWindow, only what the OBB path touches."""

    cfg = load_config(SOFTWARE_CONFIG_FILE)
    load_finished = False

    def set_saved_state(self, state):
        pass


def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    scene = AnnotationScene(StubMainWindow())
    scene.setSceneRect(0, 0, 100, 100)

    # 같은 위치를 두 번 클릭하면 첫 변의 길이가 0 이 된다
    degenerate = OBB()
    scene.addItem(degenerate)
    for x, y in [(30, 30), (30, 30), (70, 70)]:
        degenerate.addPoint(QtCore.QPointF(x, y))

    assert len(degenerate.points) == 2, (
        f"세 번째 점이 되돌려지지 않았다: {len(degenerate.points)}"
    )
    assert degenerate.is_drawing is True, "완성되지 않았는데 drawing 상태가 풀렸다"

    # 정상 입력은 그대로 4 코너로 완성되어야 한다
    normal = OBB()
    scene.addItem(normal)
    for x, y in [(10, 10), (50, 10), (50, 40)]:
        normal.addPoint(QtCore.QPointF(x, y))

    assert len(normal.points) == 4, f"정상 OBB 가 완성되지 않았다: {len(normal.points)}"
    assert normal.is_drawing is False, "정상 OBB 인데 drawing 상태가 남았다"
    assert normal.area > 0, f"면적이 계산되지 않았다: {normal.area}"

    print("OBB degenerate guard OK")
    del app


if __name__ == "__main__":
    main()
