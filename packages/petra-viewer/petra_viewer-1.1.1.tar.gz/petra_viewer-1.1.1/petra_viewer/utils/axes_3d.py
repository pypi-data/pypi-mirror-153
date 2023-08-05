from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import OpenGL.GL as ogl
import numpy as np

class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, X, Y, Z, text):
        gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
        self.text = text
        self.X = X
        self.Y = Y
        self.Z = Z

    # ---------------------------------------------------------------------
    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    # ---------------------------------------------------------------------
    def setText(self, text):
        self.text = text
        self.update()

    # ---------------------------------------------------------------------
    def moveTo(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

        self.update()

    # ---------------------------------------------------------------------
    def paint(self):
        self.GLViewWidget.qglColor(QtCore.Qt.black)
        self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)


# ---------------------------------------------------------------------
class Custom3DAxis(gl.GLAxisItem):
    """Class defined to extend 'gl.GLAxisItem'."""
    def __init__(self, parent, color=(0, 0, 0, .6)):
        gl.GLAxisItem.__init__(self)
        self.parent = parent
        self.c = color

        x, y, z = self.size()

        self.xLabel = CustomTextItem(X=x, Y=-y, Z=-z, text='')
        self.xLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.xLabel)

        #Y label
        self.yLabel = CustomTextItem(X=-x, Y=y, Z=-z, text='')
        self.yLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.yLabel)

        #Z label
        self.zLabel = CustomTextItem(X=-x, Y=-y, Z=z, text='')
        self.zLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.zLabel)

    # ---------------------------------------------------------------------
    def set_x_label(self, label=''):
        if not (hasattr(gl.GLViewWidget(), 'qglColor') and hasattr(gl.GLViewWidget(), 'renderText')):
            return

        x, y, z = self.size()

        #X label
        self.xLabel.setText(label)
        self.xLabel.moveTo(0.75*x, -y/20, -z/20)

    # ---------------------------------------------------------------------
    def set_y_label(self, label=''):
        if not (hasattr(gl.GLViewWidget(), 'qglColor') and hasattr(gl.GLViewWidget(), 'renderText')):
            return

        x, y, z = self.size()

        # X label
        self.yLabel.setText(label)
        self.yLabel.moveTo(-x / 20, 0.75 * y, -z / 20)

    # ---------------------------------------------------------------------
    def set_z_label(self, label=''):
        if not (hasattr(gl.GLViewWidget(), 'qglColor') and hasattr(gl.GLViewWidget(), 'renderText')):
            return

        x, y, z = self.size()

        # Z label
        self.zLabel.setText(label)
        self.zLabel.moveTo(-x/20, -y/20, 0.75*z)

    # ---------------------------------------------------------------------
    def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
        """Adds ticks values."""
        if not (hasattr(gl.GLViewWidget(), 'qglColor') and hasattr(gl.GLViewWidget(), 'renderText')):
            return

        x,y,z = self.size()
        xtpos = np.linspace(0, x, len(xticks))
        ytpos = np.linspace(0, y, len(yticks))
        ztpos = np.linspace(0, z, len(zticks))
        #X label
        for i, xt in enumerate(xticks):
            val = CustomTextItem(X=xtpos[i], Y=-y/20, Z=-z/20, text=str(xt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        #Y label
        for i, yt in enumerate(yticks):
            val = CustomTextItem(X=-x/20, Y=ytpos[i], Z=-z/20, text=str(yt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        #Z label
        for i, zt in enumerate(zticks):
            val = CustomTextItem(X=-x/20, Y=-y/20, Z=ztpos[i], text=str(zt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)

    # ---------------------------------------------------------------------
    def paint(self):
        self.setupGLState()
        if self.antialias:
            ogl.glEnable(ogl.GL_LINE_SMOOTH)
            ogl.glHint(ogl.GL_LINE_SMOOTH_HINT, ogl.GL_NICEST)
        ogl.glBegin(ogl.GL_LINES)

        x,y,z = self.size()
        #Draw Z
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, 0, z)
        #Draw Y
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, y, 0)
        #Draw X
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(x, 0, 0)
        ogl.glEnd()