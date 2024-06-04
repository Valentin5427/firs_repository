#coding=utf-8
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from electrolab.gui.dpgrid import DPGrid

class DPGridPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        QPyDesignerCustomWidgetPlugin.__init__(self, parent)
        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return DPGrid(parent)

    def name(self):
        return "DPGrid"

    def group(self):
        return "Custom Input Widgets"

    def includeFile(self):
        return "electrolab.gui.dpgrid"

    def isContainer(self):
        return True

