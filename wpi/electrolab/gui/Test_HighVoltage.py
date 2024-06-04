import sys
import random
from functools import partial
from PyQt4 import QtCore, QtGui #, QtWidgets


def calculate_color(model, row):
    max_value = int(model.index(row, 2).data())
    current_value = int(model.index(row, 3).data())
    if current_value == 0:
        return QtGui.QBrush(QtCore.Qt.white)
    elif max_value == current_value:
        return QtGui.QBrush(QtCore.Qt.green)
    else:
        return QtGui.QBrush(QtCore.Qt.yellow)


class IdentityProxyModel(QtCore.QIdentityProxyModel):
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and index.column() in (2, 3):
            sm = self.sourceModel()
            row = index.row()
            color = calculate_color(sm, row)
            if color is not None and color != index.data(QtCore.Qt.BackgroundRole):
                for i in range(sm.columnCount()):
                    sm.setData(sm.index(row, i), color, QtCore.Qt.BackgroundRole)
        return super(IdentityProxyModel, self).data(index, role)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.tableView = QtWidgets.QTableView()
        self.setCentralWidget(self.tableView)

        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Prod Name", "EAN","Quanyity", "Counted"])

        proxy = IdentityProxyModel(self)
        proxy.setSourceModel(self.model)
        self.tableView.setModel(proxy)

        data = [["Prod1", "123456", 0, 0],
                ["Prod2", "234567", 0, 0],
                ["Prod3", "345678", 0, 0]]

        for r, rowData in enumerate(data):
            for c, d in enumerate(rowData):
                it = QtGui.QStandardItem(str(d))
                self.model.setItem(r, c, it)

        # launch test
        for i in range(self.model.rowCount()):
            self.reset(i)

    def reset(self, row):
        max_value = random.randint(1, 10)
        self.model.item(row, 2).setText(str(max_value))
        self.model.item(row, 3).setText("0")
        QtCore.QTimer.singleShot(1000, partial(self.start_test, row))

    def start_test(self, row):
        max_value = int(self.model.item(row, 2).text())
        time_line = QtCore.QTimeLine(1000*max_value, self)
        time_line.setFrameRange(0, max_value)
        time_line.frameChanged.connect(partial(self.update_value, row))
        # reset after 3 seconds of completion
        time_line.finished.connect(lambda r=row: QtCore.QTimer.singleShot(3000, partial(self.reset, r)))
        time_line.start()

    def update_value(self, r, i):
        model = self.tableView.model()
        ix = model.index(r, 3)
        model.setData(ix, str(i))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())        