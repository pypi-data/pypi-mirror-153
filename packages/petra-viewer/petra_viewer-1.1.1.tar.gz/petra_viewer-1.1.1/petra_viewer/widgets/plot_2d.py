# Created by matveyev at 28.10.2021

from silx.gui.plot.PlotWindow import Plot2D, items
from silx.utils.weakref import WeakMethodProxy


class Plot2DWithRoi(Plot2D):

    def __init__(self, parent=None, backend=None):
        posInfo = [
            ('X', lambda x, y: x),
            ('Y', lambda x, y: y),
            ('Data', WeakMethodProxy(self._getImageValue)),
            ('Dims', WeakMethodProxy(self._getImageDims)),
        ]

        super(Plot2D, self).__init__(parent=parent, backend=backend,
                                     resetzoom=True, autoScale=False,
                                     logScale=False, grid=False,
                                     curveStyle=False, colormap=True,
                                     aspectRatio=True, yInverted=False,
                                     copy=True, save=True, print_=True,
                                     control=False, position=posInfo,
                                     roi=True, mask=False)
        self.setWindowTitle('Plot2D')

        # self.profile = ProfileToolBar(plot=self)
        # self.addToolBar(self.profile)

        self.colorbarAction.setVisible(True)
        self.getColorBarWidget().setVisible(True)

        # Put colorbar action after colormap action
        actions = self.toolBar().actions()
        for action in actions:
            if action is self.getColormapAction():
                break

        self.sigActiveImageChanged.connect(self.__activeImageChanged)

    def __activeImageChanged(self, previous, legend):
        """Handle change of active image

        :param Union[str,None] previous: Legend of previous active image
        :param Union[str,None] legend: Legend of current active image
        """
        if previous is not None:
            item = self.getImage(previous)
            if item is not None:
                item.sigItemChanged.disconnect(self.__imageChanged)

        if legend is not None:
            item = self.getImage(legend)
            item.sigItemChanged.connect(self.__imageChanged)

        positionInfo = self.getPositionInfoWidget()
        if positionInfo is not None:
            positionInfo.updateInfo()

    def __imageChanged(self, event):
        """Handle update of active image item

        :param event: Type of changed event
        """
        if event == items.ItemChangedType.DATA:
            positionInfo = self.getPositionInfoWidget()
            if positionInfo is not None:
                positionInfo.updateInfo()

