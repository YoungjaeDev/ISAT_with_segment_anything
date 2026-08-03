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


def assert_handle_on_corner(obb, index, label):
    """Fail when the draggable handle drifted away from the corner it owns."""
    handle = obb.vertices[index].pos()
    corner = obb.mapToScene(obb.points[index])
    assert (round(handle.x(), 3), round(handle.y(), 3)) == (
        round(corner.x(), 3),
        round(corner.y(), 3),
    ), (
        f"{label}: 핸들이 코너에서 떨어졌다 "
        f"handle=({handle.x()}, {handle.y()}) corner=({corner.x()}, {corner.y()})"
    )


def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    scene = AnnotationScene(StubMainWindow())
    scene.setSceneRect(0, 0, 100, 100)

    # 같은 위치를 두 번 클릭하면 첫 변의 길이가 0 이 된다
    degenerate = OBB()
    scene.addItem(degenerate)
    for x, y in [(30, 30), (30, 30), (70, 70)]:
        degenerate.addPoint(QtCore.QPointF(x, y))

    # 앵커 2 개 + 마우스를 따라다니는 trailing 1 개가 남아야 한다
    assert len(degenerate.points) == 3, (
        f"거부 후 상태가 앵커 2 + trailing 1 이 아니다: {len(degenerate.points)}"
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
    # 네 번째 핸들을 놓는 과정에서 코너가 재계산되어 순서가 뒤집히면 안 된다
    first_edge = [(p.x(), p.y()) for p in normal.points[:2]]
    assert first_edge == [(10.0, 10.0), (50.0, 10.0)], (
        f"완성 후 첫 변이 바뀌었다: {first_edge}"
    )

    # 세 번째 점이 첫 변 위에 있으면 높이가 0 인 사각형이 된다
    flat = OBB()
    scene.addItem(flat)
    for x, y in [(10, 60), (60, 60), (35, 60)]:
        flat.addPoint(QtCore.QPointF(x, y))

    assert len(flat.points) == 3, (
        f"높이 0 인 완성이 적용됐다: {[(p.x(), p.y()) for p in flat.points]}"
    )
    assert flat.is_drawing is True, "완성되지 않았는데 drawing 상태가 풀렸다"

    # 세 클릭이 모두 이미지 안이어도 투영된 코너는 밖으로 나갈 수 있다
    projected_out = OBB()
    scene.addItem(projected_out)
    for x, y in [(0, 50), (99, 0), (0, 0)]:
        projected_out.addPoint(QtCore.QPointF(x, y))

    assert len(projected_out.points) == 3, (
        f"이미지를 벗어나는 완성이 적용됐다: "
        f"{[(p.x(), p.y()) for p in projected_out.points]}"
    )
    assert projected_out.is_drawing is True, "완성되지 않았는데 drawing 상태가 풀렸다"
    # 두 앵커가 그대로여야 다음 클릭에서 첫 변이 바뀌지 않는다
    anchors = [(p.x(), p.y()) for p in projected_out.points[:2]]
    assert anchors == [(0.0, 50.0), (99.0, 0.0)], f"앵커가 바뀌었다: {anchors}"

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

    # 회전된 OBB 의 코너를 끌 때, 파생 코너가 밖으로 나가는 드래그는 거부되고
    # 그래픽 핸들도 도형에서 떨어지지 않아야 한다
    drag = OBB()
    scene.addItem(drag)
    for x, y in [(50, 10), (70, 30), (60, 40)]:
        drag.addPoint(QtCore.QPointF(x, y))
    assert len(drag.points) == 4, "회전된 OBB 가 완성되지 않았다"

    before_drag = [(p.x(), p.y()) for p in drag.points]
    drag.vertices[0].setPos(QtCore.QPointF(0, 99))
    after_drag = [(p.x(), p.y()) for p in drag.points]
    assert before_drag == after_drag, f"이미지를 벗어나는 드래그가 적용됐다: {after_drag}"
    assert_handle_on_corner(drag, 0, "경계를 벗어나는 드래그")

    # 대각선을 한 축에 눕히면 인접 코너가 붕괴해 면적 0 이 된다
    drag.vertices[0].setPos(QtCore.QPointF(45, 55))
    flattened = [(p.x(), p.y()) for p in drag.points]
    assert before_drag == flattened, f"면적 0 을 만드는 드래그가 적용됐다: {flattened}"
    assert_handle_on_corner(drag, 0, "면적을 없애는 드래그")

    # 여유 있는 위치로 끄는 것은 정상 반영되어야 한다
    drag.vertices[0].setPos(QtCore.QPointF(48, 12))
    moved = [(p.x(), p.y()) for p in drag.points]
    assert moved != before_drag, "여유 있는 드래그인데 반영되지 않았다"
    assert_handle_on_corner(drag, 0, "수락된 드래그")

    print("OBB degenerate guard OK")
    del app


if __name__ == "__main__":
    main()
