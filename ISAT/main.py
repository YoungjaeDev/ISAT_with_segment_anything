# -*- coding: utf-8 -*-
# @Author  : LG
# import os

import sys

# PyQt5 가 번들한 구버전 MSVC 런타임이 먼저 올라가면 torch 의 c10.dll 이 WinError 1114 로 죽는다.
# torch 를 항상 PyQt5 보다 먼저 import 한다.
import torch

from PyQt5 import QtWidgets

from ISAT.widgets.mainwindow import MainWindow

# ubuntu18.04装其他应用时，环境崩了。。。qtapp初始化后，torch调用cuda会卡死，但先调用下cuda就不会卡死。

torch.cuda.is_available()
# (知道怎么处理该问题，请反馈下 T.T)


def main():
    from ISAT.banner import print_banner
    print_banner()
    app = QtWidgets.QApplication([""])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
