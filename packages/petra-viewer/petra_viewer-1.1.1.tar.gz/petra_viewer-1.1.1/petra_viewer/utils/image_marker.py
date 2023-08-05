# Created by matveyev at 24.03.2021

from PyQt5 import QtCore
import pyqtgraph as pg

# ----------------------------------------------------------------------
class ImageMarker(object):
    """Infinite lines cross
    """

    # ----------------------------------------------------------------------
    def __init__(self, x, y, image_view):
        super(ImageMarker, self).__init__()

        self.image_view = image_view

        pen = pg.mkPen('y', width=1, style=QtCore.Qt.DotLine)

        self._marker_v = pg.InfiniteLine(pos=x, pen=pen)
        self.image_view.addItem(self._marker_v, ignoreBounds=True)

        self._marker_h = pg.InfiniteLine(pos=y, angle=0, pen=pen)
        self.image_view.addItem(self._marker_h, ignoreBounds=True)

    # ----------------------------------------------------------------------
    def setPos(self, pos):
        """
        """
        self._marker_v.setPos(pos.x())
        self._marker_h.setPos(pos.y())

    # ----------------------------------------------------------------------
    def pos(self):
        """
        """
        return self._marker_v.pos().x(), self._marker_h.pos().y()

    # ----------------------------------------------------------------------
    def setVisible(self, flag):
        """
        """
        self._marker_v.setVisible(flag)
        self._marker_h.setVisible(flag)

    # ----------------------------------------------------------------------
    def visible(self):
        """
        """
        return self._marker_v.isVisible() and self._marker_h.isVisible()

    # ----------------------------------------------------------------------
    def delete_me(self):
        self.image_view.removeItem(self._marker_h)
        self.image_view.removeItem(self._marker_v)