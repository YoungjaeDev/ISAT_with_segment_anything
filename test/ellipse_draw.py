# -*- coding: utf-8 -*-

"""Check the two-click ellipse draw mode.

Drives the scene through press, move, press and checks that an ordinary
Polygon lying on the inscribed ellipse is added.

Runs headless (offscreen Qt platform). Run directly:

    uv run python test/ellipse_draw.py
"""

import os
import sys
from unittest.mock import MagicMock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5 import QtCore, QtGui, QtWidgets

from ISAT.configs import SOFTWARE_CONFIG_FILE, STATUSMode, load_config
from ISAT.widgets.canvas import AnnotationScene
from ISAT.widgets.polygon import Polygon


def make_scene():
    """Build a scene over a permissive MainWindow stand-in."""
    mainwindow = MagicMock()
    mainwindow.cfg = load_config(SOFTWARE_CONFIG_FILE)
    mainwindow.load_finished = False
    mainwindow.polygons = []
    mainwindow.current_category = "bowl"
    mainwindow.current_group = 1
    mainwindow.group_select_mode = "manual"
    mainwindow.category_color_dict = {}
    scene = AnnotationScene(mainwindow)
    scene.setSceneRect(0, 0, 100, 100)
    # 이미지가 없으면 create 모드로 들어가지 않는다
    scene.image_item = scene.addPixmap(QtGui.QPixmap(100, 100))
    # 뷰를 scene 에 매달아 두어야 수거되지 않는다
    scene.view = QtWidgets.QGraphicsView(scene)
    scene.view.resize(300, 300)
    return scene, mainwindow


def send(scene, kind, x, y):
    """Deliver a left-button mouse event at scene position (x, y) through the view."""
    view = scene.views()[0]
    pressed = kind != QtCore.QEvent.MouseMove
    event = QtGui.QMouseEvent(
        kind,
        QtCore.QPointF(view.mapFromScene(QtCore.QPointF(x, y))),
        QtCore.Qt.MouseButton.LeftButton if pressed else QtCore.Qt.MouseButton.NoButton,
        QtCore.Qt.MouseButton.LeftButton if kind == QtCore.QEvent.MouseButtonPress else QtCore.Qt.MouseButton.NoButton,
        QtCore.Qt.KeyboardModifier.NoModifier,
    )
    QtWidgets.QApplication.sendEvent(view.viewport(), event)


def click(scene, x, y):
    """Press and release the left button at scene position (x, y)."""
    send(scene, QtCore.QEvent.MouseButtonPress, x, y)
    send(scene, QtCore.QEvent.MouseButtonRelease, x, y)


def draw(scene, corner_a, corner_b):
    """Click corner_a, move to corner_b, click corner_b."""
    scene.start_draw_ellipse()
    click(scene, *corner_a)
    send(scene, QtCore.QEvent.MouseMove, *corner_b)
    click(scene, *corner_b)


def assert_on_ellipse(polygon, cx, cy, rx, ry, label):
    """Fail unless the polygon is 36 points on the given ellipse touching its box."""
    pts = [(p.x(), p.y()) for p in polygon.points]
    assert len(pts) == 36, f"{label}: 꼭짓점이 36 개가 아니다: {len(pts)}"
    for x, y in pts:
        value = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
        assert abs(value - 1) < 1e-6, f"{label}: 타원 위에 없는 점 ({x}, {y})"
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    box = [round(v, 6) for v in (min(xs), min(ys), max(xs), max(ys))]
    assert box == [cx - rx, cy - ry, cx + rx, cy + ry], f"{label}: 박스에 꽉 차지 않는다: {box}"
    assert len(set(pts)) == 36, f"{label}: 겹치는 꼭짓점이 있다"


def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    # 박스 (20,10)-(80,50) 에 꽉 차는 타원: 중심 (50,30), 반지름 30 x 20
    scene, mainwindow = make_scene()
    draw(scene, (20, 10), (80, 50))
    assert len(mainwindow.polygons) == 1, f"폴리곤이 추가되지 않았다: {len(mainwindow.polygons)}"
    polygon = mainwindow.polygons[0]
    assert type(polygon) is Polygon, f"일반 Polygon 이 아니다: {type(polygon)}"
    assert_on_ellipse(polygon, 50, 30, 30, 20, "타원")
    assert polygon.category == "bowl", f"카테고리가 설정되지 않았다: {polygon.category}"
    assert polygon.is_drawing is False, "완성됐는데 drawing 상태가 남았다"
    assert len(polygon.vertices) == 36, f"핸들 수가 점 수와 다르다: {len(polygon.vertices)}"
    assert scene.mode == STATUSMode.VIEW, f"완성 후 view 모드로 돌아오지 않았다: {scene.mode}"

    # 오른쪽 아래에서 왼쪽 위로 그려도 같은 타원이어야 한다
    scene, mainwindow = make_scene()
    draw(scene, (80, 50), (20, 10))
    assert len(mainwindow.polygons) == 1, "역방향으로 그리면 폴리곤이 추가되지 않는다"
    assert_on_ellipse(mainwindow.polygons[0], 50, 30, 30, 20, "역방향 타원")

    # Shift 를 누르면 짧은 변(40)에 맞춘 정사각형이 되어 정원: 중심 (40,30), 반지름 20
    scene, mainwindow = make_scene()
    scene.shift_pressed = True
    draw(scene, (20, 10), (80, 50))
    assert len(mainwindow.polygons) == 1, "Shift 상태에서 폴리곤이 추가되지 않았다"
    assert_on_ellipse(mainwindow.polygons[0], 40, 30, 20, 20, "정원")

    # 같은 자리를 두 번 클릭하면 크기가 0 이므로 아무것도 추가되지 않아야 한다
    scene, mainwindow = make_scene()
    draw(scene, (30, 30), (30, 30))
    assert mainwindow.polygons == [], "크기 0 인 타원이 추가됐다"

    # 그리던 중 취소하면 다음 번에 이전 앵커가 남아 있지 않아야 한다
    scene, mainwindow = make_scene()
    scene.start_draw_ellipse()
    click(scene, 5, 5)
    scene.cancel_draw()
    draw(scene, (20, 10), (80, 50))
    assert len(mainwindow.polygons) == 1, "취소 후 다시 그리면 폴리곤이 추가되지 않는다"
    assert_on_ellipse(mainwindow.polygons[0], 50, 30, 30, 20, "취소 후 타원")

    print("ok")
    del app


if __name__ == "__main__":
    main()
