from pyqtgraph.graphicsItems.LegendItem import LegendItem

class MatveyevLegend(LegendItem):

    def __init__(self, size=None, offset=None):
        super(MatveyevLegend, self).__init__(size, offset)

    def removeItemByAddress(self, item):
        for sample, label in self.items:
            if sample.item == item:  # !
                self.items.remove((sample, label))
                self.layout.removeItem(sample)
                sample.close()
                self.layout.removeItem(label)
                label.close()
                self.updateSize()

def addLegend(plot_item, size=None, offset=(30, 30)):

    plot_item.legend = MatveyevLegend(size, offset)
    plot_item.legend.setParentItem(plot_item.vb)
    return plot_item.legend
