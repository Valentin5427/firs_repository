#coding=utf-8
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from electrolab.gui.ellipsiscombobox import EllipsisComboBox

class EllipsisComboBoxPlugin(QPyDesignerCustomWidgetPlugin):

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
      return EllipsisComboBox(parent)

   def name(self):
      return "EllipsisComboBox"

   def group(self):
      return "Custom Input Widgets"

   def includeFile(self):
      return "electrolab.gui.ellipsiscombobox"

   def isContainer(self):
        return False

