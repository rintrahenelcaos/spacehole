import functools
from PyQt5 import QtCore, QtGui, QtWidgets


def helper_function(widget, color):
    widget.setStyleSheet("background-color: {}".format(color.name()))


def apply_color_animation(widget, start_color, end_color, duration=1000):
    anim = QtCore.QVariantAnimation(
        widget,
        duration=duration,
        startValue=start_color,
        endValue=end_color,
        loopCount=2,
    )
    anim.valueChanged.connect(functools.partial(helper_function, widget))
    anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)


class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()

        self.button = QtWidgets.QFrame()
        self.button.setGeometry(QtCore.QRect(0,0, 60,60))

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.button)

        timer = QtCore.QTimer(self, interval=5 * 1000)
        timer.timeout.connect(self.handle_timeout)
        timer.start()
        self.handle_timeout()

    def handle_timeout(self):
        apply_color_animation(
            self.button,
            QtGui.QColor("lightgreen"),
            QtGui.QColor("darkgreen"),
            duration=2500,
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Widget()
    w.show()
    sys.exit(app.exec_())