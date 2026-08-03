# -*- coding: utf-8 -*-

"""Check the OBB guards against degenerate geometry.

Covers a zero-length first edge (division by zero on completion) and a
rotation that would push corners outside the image.

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

    # 세 클릭이 모두 이미지 안이어도 투영된 코너는 밖으로 나갈 수 있다
    projected_out = OBB()
    scene.addItem(projected_out)
    for x, y in [(0, 50), (99, 0), (0, 0)]:
        projected_out.addPoint(QtCore.QPointF(x, y))

    assert len(projected_out.points) == 2, (
        f"이미지를 벗어나는 완성이 적용됐다: "
        f"{[(p.x(), p.y()) for p in projected_out.points]}"
    )
    assert projected_out.is_drawing is True, "완성되지 않았는데 drawing 상태가 풀렸다"

    # 이미지를 꽉 채운 OBB 는 회전하면 코너가 밖으로 나가므로 회전을 거부해야 한다
    edge = OBB()
    scene.addItem(edge)
    for x, y in [(0, 0), (99, 0), (99, 99)]:
        edge.addPoint(QtCore.QPointF(x, y))
    assert len(edge.points) == 4, "경계 OBB 가 완성되지 않았다"

    before = [(p.x(), p.y()) for p in edge.points]
    edge.rotate(0.3)
    after = [(p.x(), p.y()) for p in edge.points]
    assert before == after, f"이미지를 벗어나는 회전이 적용됐다: {after}"

    # 여유가 있는 OBB 는 정상적으로 회전해야 한다
    inner = OBB()
    scene.addItem(inner)
    for x, y in [(40, 40), (60, 40), (60, 55)]:
        inner.addPoint(QtCore.QPointF(x, y))
    inner_before = [(p.x(), p.y()) for p in inner.points]
    inner.rotate(0.3)
    inner_after = [(p.x(), p.y()) for p in inner.points]
    assert inner_before != inner_after, "여유가 있는 OBB 인데 회전하지 않았다"

    print("OBB degenerate guard OK")
    del app


if __name__ == "__main__":
    main()
