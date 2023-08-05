# Created by matveyev at 17.02.2021

from PyQt5 import QtGui, QtWidgets
import pyqtgraph as pg
import petra_viewer.lookandfeel as lookandfeel
from petra_viewer.utils.utils import get_text_coordinates

# ----------------------------------------------------------------------
class CrosshairCursor(object):

    # ----------------------------------------------------------------------
    def __init__(self, plot_item):
        self.visible = False
        self.plot_item = plot_item

        line_style = lookandfeel.CROSSHAIR_CURSOR["line_style"]
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen(line_style))
        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen(line_style))

        plot_item.addItem(self.vline, ignoreBounds=True)
        plot_item.addItem(self.hline, ignoreBounds=True)

        text_style = lookandfeel.CROSSHAIR_CURSOR["text_style"]
        self.label = pg.TextItem(text="", color=text_style["color"], fill=text_style["fill"])
        self.label.setFont(QtGui.QFont(*text_style["font"]))
        plot_item.addItem(self.label, ignoreBounds=True)

    # ----------------------------------------------------------------------
    def setPos(self, x_label, x, y):
        if self.visible:
            msg = "{}: {}, Value: {}".format(x_label, self.niceNumber(x), self.niceNumber(y))
            self.label.setText(msg, color=lookandfeel.CROSSHAIR_CURSOR["text_style"]["color"])
            self.label.setPos(get_text_coordinates(self.plot_item, self.label.boundingRect(), 'br'))
            self.vline.setPos(x)
            self.hline.setPos(y)

    # ----------------------------------------------------------------------
    def setVisible(self, flag):
        self.visible = flag
        self.vline.setVisible(flag)
        self.hline.setVisible(flag)
        self.label.setVisible(flag)

    # ----------------------------------------------------------------------
    @staticmethod
    def niceNumber(number):
        knumber = number // 1000
        mnumber = knumber // 1000
        gnumber = mnumber // 1000
        if knumber == 0:
            return "{:.2f}".format(number)
        elif mnumber == 0:
            return "{:.2f} K".format(number/1000.)
        elif gnumber == 0:
            return "{:.2f} M".format(float(number)/1e6)

        return "{:.2f} G".format(float(number)/1e9)


# ----------------------------------------------------------------------
class Ruler(object):

    # ----------------------------------------------------------------------
    def __init__(self, plot_item):

        self.enabled = False
        self.during_measurement = False

        self.plot_item = plot_item

        vert_line = lookandfeel.DISTANCE_MEASUREMENT["vertical_line"]
        self.vline_first = pg.InfiniteLine(angle=90, movable=False, pen=vert_line)
        plot_item.addItem(self.vline_first, ignoreBounds=True)

        self.vline_second = pg.InfiniteLine(angle=90, movable=False, pen=vert_line)
        plot_item.addItem(self.vline_second, ignoreBounds=True)

        self.hline = QtWidgets.QGraphicsLineItem()
        self.hline.setPen(pg.mkPen(lookandfeel.DISTANCE_MEASUREMENT["horizontal_line"]))
        plot_item.addItem(self.hline, ignoreBounds=True)

        arrow_style = lookandfeel.DISTANCE_MEASUREMENT["arrow_style"]
        self.left_arrow = pg.ArrowItem(angle=0, **arrow_style)
        plot_item.addItem(self.left_arrow)
        self.right_arrow = pg.ArrowItem(angle=180, **arrow_style)
        plot_item.addItem(self.right_arrow)

        text_style = lookandfeel.DISTANCE_MEASUREMENT["text_style"]
        self.label = pg.TextItem(text="", color=text_style["color"], fill=text_style["fill"])
        self.label.setFont(QtGui.QFont(*text_style["font"]))
        plot_item.addItem(self.label, ignoreBounds=True)

        self.setVisible(False)

    # ----------------------------------------------------------------------
    def mouseClicked(self, x, y):
        if self.enabled:
            if self.during_measurement:
                self.stopMeasurement(x, y)
            else:
                self.startMeasurement(x, y)
        else:
            self.disableMeasurement()

    # ----------------------------------------------------------------------

    def startMeasurement(self, x, y):
        self.during_measurement = True
        self.label.setText("0.0", color=lookandfeel.DISTANCE_MEASUREMENT["text_style"]["color"])
        # self.label.setPos(get_text_coordinates(self.plot_item, self.label.boundingRect(), xinfo, 'br'))

        self.label.setPos(x - self.label.boundingRect().width() *
                          self.plot_item.getViewBox().viewPixelSize()[0] / 2, y)

        self.start_x, self.start_y = x, y

        self.vline_first.setPos(x)
        self.vline_second.setPos(x)
        self.hline.setLine(x, y, x, y)
        self.left_arrow.setPos(x, y)
        self.right_arrow.setPos(x, y)

        self.setVisible(True)

    # ----------------------------------------------------------------------
    def stopMeasurement(self, x, y):
        dx = x - self.start_x
        txt = "{:.4f}".format(dx)
        self.label.setText(txt, color=lookandfeel.DISTANCE_MEASUREMENT["text_style"]["color"])
        # self.label.setPos(get_text_coordinates(self.plot_item, self.label.boundingRect(), xinfo, 'br'))
        self.label.setPos((x + self.start_x) / 2 - self.label.boundingRect().width() *
                          self.plot_item.getViewBox().viewPixelSize()[0] / 2, self.start_y)

        line = self.hline.line()
        self.hline.setLine(line.x1(), line.y1(), x, line.y1())

        self.during_measurement = False

    # ----------------------------------------------------------------------
    def disableMeasurement(self):
        self.during_measurement = False
        self.setVisible(False)

    # ----------------------------------------------------------------------
    def mouseMoved(self, x, y):
        if self.enabled and self.during_measurement:
            self.redraw(x, y)

    # ----------------------------------------------------------------------
    def redraw(self, x, y):
        """Show distance info (during measurement)
        """
        dx = x - self.start_x
        txt = "{:.4f}".format(dx)
        self.label.setText(txt, color=lookandfeel.DISTANCE_MEASUREMENT["text_style"]["color"])
        self.label.setPos((x + self.start_x) / 2 - self.label.boundingRect().width() *
                          self.plot_item.getViewBox().viewPixelSize()[0] / 2, self.start_y)

        line = self.hline.line()
        self.hline.setLine(line.x1(), line.y1(), x, line.y1())

        if dx > 0:
            self.left_arrow.setPos(self.start_x, self.start_y)
            self.right_arrow.setPos(x, line.y1())
        else:
            self.right_arrow.setPos(self.start_x, self.start_y)
            self.left_arrow.setPos(x, line.y1())

        self.vline_second.setPos(x)

    # ----------------------------------------------------------------------
    def setEnabled(self, flag):
        self.enabled = flag
        if not flag:
            self.setVisible(flag)

    # ----------------------------------------------------------------------
    def setVisible(self, flag):
        self.vline_first.setVisible(flag)
        self.vline_second.setVisible(flag)
        self.hline.setVisible(flag)
        self.label.setVisible(flag)
        self.left_arrow.setVisible(flag)
        self.right_arrow.setVisible(flag)

