import sys
from PyQt4 import QtGui
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class Qt4MplCanvas(FigureCanvas):
  def __init__(self):
    self.fig=Figure()
    self.axes=self.fig.add_subplot(111)
    self.axes.plot([1,2,3,4], [1,4,9,16], 'r-')
    self.axes.axis([0, 6, 0, 20])

    FigureCanvas.__init__(self,self.fig)

if __name__ == '__main__':
  qApp=QtGui.QApplication(sys.argv)
  mpl=Qt4MplCanvas()
  mpl.show()
  sys.exit(qApp.exec_())