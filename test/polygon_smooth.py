# -*- coding: utf-8 -*-

"""Check the outline smoothing of a selected polygon (G) and its restore (Shift+G).

Builds a jittery polygon in the scene, smooths it through the key handler and
checks that the jitter is gone while the shape, the vertex count and the
handles stay consistent.

Runs headless (offscreen Qt platform). Run directly:

    uv run python test/polygon_smooth.py
"""

import math
import os
import sys
from unittest.mock import MagicMock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5 import QtCore, QtGui, QtWidgets

from ISAT.configs import SOFTWARE_CONFIG_FILE, STATUSMode, load_config
from ISAT.widgets.canvas import AnnotationScene, AnnotationView
from ISAT.widgets.polygon import Polygon, smooth_closed_points


def jittery_circle(cx, cy, r, n=72, jitter=1.0):
    """Circle whose radius alternates by +-jitter, like a shaky hand-drawn line."""
    return [
        (
            cx + (r + (jitter if i % 2 else -jitter)) * math.cos(2 * math.pi * i / n),
            cy + (r + (jitter if i % 2 else -jitter)) * math.sin(2 * math.pi * i / n),
        )
        for i in range(n)
    ]


def radial_error(points, cx, cy, r):
    return max(abs(math.hypot(x - cx, y - cy) - r) for x, y in points)


def make_scene():
    """Build a scene and a view over a permissive MainWindow stand-in."""
    mainwindow = MagicMock()
    mainwindow.cfg = load_config(SOFTWARE_CONFIG_FILE)
    mainwindow.load_finished = True
    mainwindow.polygons = []
    mainwindow.category_color_dict = {}
    scene = AnnotationScene(mainwindow)
    scene.setSceneRect(0, 0, 200, 200)
    scene.image_item = scene.addPixmap(QtGui.QPixmap(200, 200))
    scene.view = AnnotationView()
    scene.view.setScene(scene)
    return scene, mainwindow


def add_polygon(scene, mainwindow, points):
    polygon = Polygon()
    scene.addItem(polygon)
    for x, y in points:
        polygon.addPoint(QtCore.QPointF(x, y))
    polygon.set_drawed("bowl", 1, False, "", QtGui.QColor("#ff0000"), 1)
    polygon.redraw()
    mainwindow.polygons.append(polygon)
    return polygon


def press(scene, key, modifier=QtCore.Qt.KeyboardModifier.NoModifier):
    event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, modifier)
    QtWidgets.QApplication.sendEvent(scene.view, event)


def xy(polygon):
    return [(p.x(), p.y()) for p in polygon.points]


def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    # 순수 함수: 떨림(+-1)은 줄고 꼭짓점 수는 그대로다
    before = jittery_circle(100, 100, 60)
    after = smooth_closed_points(before)
    assert len(after) == len(before), f"꼭짓점 수가 바뀌었다: {len(after)}"
    assert radial_error(before, 100, 100, 60) > 0.99, "입력에 떨림이 없다"
    assert radial_error(after, 100, 100, 60) < 0.3, f"떨림이 남았다: {radial_error(after, 100, 100, 60)}"

    # 순수 함수: 네모는 네모로 남는다(모서리가 조금 둥글어질 뿐 타원이 되지 않는다)
    square = [(40 + 6 * i, 40) for i in range(20)] + [(160, 40 + 6 * i) for i in range(20)]
    square += [(160 - 6 * i, 160) for i in range(20)] + [(40, 160 - 6 * i) for i in range(20)]
    smoothed = smooth_closed_points(square)
    corner = min(math.hypot(x - 40, y - 40) for x, y in smoothed)
    assert corner < 6, f"모서리가 너무 깎였다: {corner}"
    assert all(39.9 <= x <= 160.1 and 39.9 <= y <= 160.1 for x, y in smoothed), "네모 밖으로 나간 점이 있다"

    # 순수 함수: 점이 3개 미만이거나 둘레가 0 이면 그대로 돌려준다
    assert smooth_closed_points([(1, 1), (2, 2)]) == [(1, 1), (2, 2)], "점 2개가 바뀌었다"
    assert smooth_closed_points([(5, 5)] * 4) == [(5, 5)] * 4, "둘레 0 인 폴리곤이 바뀌었다"

    # G 키: 선택한 폴리곤만 펴지고, 핸들이 점을 따라가며, 저장 안 됨 상태가 된다
    scene, mainwindow = make_scene()
    target = add_polygon(scene, mainwindow, jittery_circle(60, 60, 40))
    other = add_polygon(scene, mainwindow, jittery_circle(140, 140, 40))
    original, untouched = xy(target), xy(other)
    target.setSelected(True)
    mainwindow.set_saved_state.reset_mock()
    press(scene, QtCore.Qt.Key.Key_G)
    assert radial_error(xy(target), 60, 60, 40) < 0.3, "G 키로 떨림이 줄지 않았다"
    assert xy(other) == untouched, "선택하지 않은 폴리곤이 바뀌었다"
    assert len(target.vertices) == len(target.points) == 72, "핸들 수와 점 수가 어긋났다"
    for vertex, point in zip(target.vertices, target.points):
        assert (vertex.pos() - point).manhattanLength() < 1e-6, "핸들이 점을 따라가지 않았다"
    assert target.polygon().count() == 72, "그려진 도형이 갱신되지 않았다"
    mainwindow.set_saved_state.assert_called_with(False)

    # Shift+G: 여러 번 편 뒤에도 처음 모양으로 돌아온다
    press(scene, QtCore.Qt.Key.Key_G)
    press(scene, QtCore.Qt.Key.Key_G, QtCore.Qt.KeyboardModifier.ShiftModifier)
    assert xy(target) == original, "Shift+G 로 처음 모양이 돌아오지 않았다"
    for vertex, point in zip(target.vertices, target.points):
        assert (vertex.pos() - point).manhattanLength() < 1e-6, "되돌린 뒤 핸들이 점과 어긋났다"

    # 옮겨 놓은 폴리곤(pos 가 0 이 아님)도 핸들이 화면 위치를 따라간다
    scene, mainwindow = make_scene()
    moved = add_polygon(scene, mainwindow, jittery_circle(60, 60, 40))
    moved.setPos(30, 20)
    moved.setSelected(True)
    press(scene, QtCore.Qt.Key.Key_G)
    for vertex, point in zip(moved.vertices, moved.points):
        assert (vertex.pos() - moved.mapToScene(point)).manhattanLength() < 1e-6, "옮긴 폴리곤의 핸들이 어긋났다"

    # 편 뒤에 윤곽을 다시 그리면(꼭짓점을 지우고 새로 넣음) 옛 모양으로 덮어쓰지 않는다
    scene, mainwindow = make_scene()
    polygon = add_polygon(scene, mainwindow, jittery_circle(60, 60, 40))
    polygon.setSelected(True)
    press(scene, QtCore.Qt.Key.Key_G)
    redrawn = jittery_circle(70, 70, 30)
    polygon.delete()
    for x, y in redrawn:
        polygon.addPoint(QtCore.QPointF(x, y))
    polygon.redraw()
    press(scene, QtCore.Qt.Key.Key_G, QtCore.Qt.KeyboardModifier.ShiftModifier)
    assert xy(polygon) == redrawn, "다시 그린 윤곽이 Shift+G 로 옛 모양이 됐다"

    # 꼭짓점을 뺀 뒤에 펴면 그 시점의 모양이 새 복원 기준이 된다
    polygon.removePoint(0)
    trimmed = xy(polygon)
    press(scene, QtCore.Qt.Key.Key_G)
    assert xy(polygon) != trimmed, "꼭짓점을 뺀 뒤 G 키가 동작하지 않았다"
    press(scene, QtCore.Qt.Key.Key_G, QtCore.Qt.KeyboardModifier.ShiftModifier)
    assert xy(polygon) == trimmed, "꼭짓점을 뺀 뒤의 모양으로 돌아오지 않았다"

    # 편 뒤 이미지 가장자리로 옮기고 되돌려도 윤곽이 이미지 밖으로 나가지 않는다
    scene, mainwindow = make_scene()
    polygon = add_polygon(scene, mainwindow, jittery_circle(100, 100, 40, jitter=10))
    polygon.setSelected(True)
    press(scene, QtCore.Qt.Key.Key_G)
    polygon.setPos(-polygon.boundingRect().left(), 0)
    press(scene, QtCore.Qt.Key.Key_G, QtCore.Qt.KeyboardModifier.ShiftModifier)
    restored = [polygon.mapToScene(p) for p in polygon.points]
    assert max(abs(math.hypot(p.x() - polygon.pos().x() - 100, p.y() - 100) - 40) for p in restored) > 9.9, "원래 모양이 돌아오지 않았다"
    assert all(-1e-6 <= p.x() <= 200 + 1e-6 and -1e-6 <= p.y() <= 200 + 1e-6 for p in restored), "되돌린 윤곽이 이미지 밖으로 나갔다"
    for vertex, point in zip(polygon.vertices, restored):
        assert (vertex.pos() - point).manhattanLength() < 1e-6, "가장자리에서 되돌린 뒤 핸들이 어긋났다"

    # VIEW 모드가 아니면 아무것도 하지 않는다
    scene, mainwindow = make_scene()
    polygon = add_polygon(scene, mainwindow, jittery_circle(60, 60, 40))
    original = xy(polygon)
    polygon.setSelected(True)
    scene.mode = STATUSMode.CREATE
    press(scene, QtCore.Qt.Key.Key_G)
    assert xy(polygon) == original, "VIEW 모드가 아닌데 폴리곤이 바뀌었다"

    print("ok")
    del app


if __name__ == "__main__":
    main()
