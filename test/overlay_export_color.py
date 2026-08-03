# -*- coding: utf-8 -*-

"""Check that export_overlay_image writes polygon colors in the right channels.

Runs headless (offscreen Qt platform). Run directly:

    uv run python test/overlay_export_color.py
"""

import os
import sys
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ISAT.configs import SOFTWARE_CONFIG_FILE, load_config
from ISAT.widgets.canvas import AnnotationScene
from ISAT.widgets.polygon import Polygon

IMAGE_SIZE = 100


class StubMainWindow:
    """Minimal stand-in for MainWindow, only what the polygon path touches."""

    cfg = load_config(SOFTWARE_CONFIG_FILE)
    load_finished = False

    def set_saved_state(self, state):
        pass


def build_scene(color: str):
    scene = AnnotationScene(StubMainWindow())
    scene.image_data = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)
    # vertex 는 sceneRect 로 클램프되므로 이미지 크기와 맞춰야 한다
    scene.setSceneRect(0, 0, IMAGE_SIZE, IMAGE_SIZE)

    polygon = Polygon()
    scene.addItem(polygon)
    polygon.color = QtGui.QColor(color)
    for x, y in [(10, 10), (90, 10), (90, 90), (10, 90)]:
        polygon.addPoint(QtCore.QPointF(x, y))
    polygon.redraw()
    polygon.is_drawing = False
    return scene


def export_and_read(scene) -> np.ndarray:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "overlay.png")
        scene.export_overlay_image(path)
        image = cv2.imread(path)
    assert image is not None, "오버레이 PNG 가 저장되지 않았다"
    assert image.shape == (IMAGE_SIZE, IMAGE_SIZE, 3), f"크기 이상: {image.shape}"
    return image


def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    red = export_and_read(build_scene("#ff0000"))
    inside, outside = red[50, 50], red[2, 2]  # cv2.imread 는 BGR 로 읽는다

    assert outside.sum() == 0, f"폴리곤 밖이 칠해졌다: {outside.tolist()}"
    assert inside.sum() > 0, "폴리곤이 그려지지 않았다"
    assert inside[2] > 0 and inside[0] == 0, (
        f"빨간 폴리곤인데 R 채널이 아닌 곳에 색이 들어갔다: BGR={inside.tolist()}"
    )

    blue = export_and_read(build_scene("#0000ff"))[50, 50]
    assert blue[0] > 0 and blue[2] == 0, (
        f"파란 폴리곤인데 B 채널이 아닌 곳에 색이 들어갔다: BGR={blue.tolist()}"
    )

    green = export_and_read(build_scene("#00ff00"))[50, 50]
    assert green[1] > 0 and green[0] == 0 and green[2] == 0, (
        f"초록 폴리곤 색이 어긋났다: BGR={green.tolist()}"
    )

    print("overlay export color OK")
    del app


if __name__ == "__main__":
    main()
