import sys
from PySide6 import QtWidgets, QtGui, QtCore, QtCharts
import numpy as np


# # import the plotting backend for embeding into tk windows 
# from matplotlib.backends.backend_tkagg import FigureCanvasAgg 


# -- Colors --
bgColor1 = '#ffffff'
bgColor2 = '#54ccff'
textColor1 = '#ffffff'
textColor2 = '#0e1778'
buttonBgColor = "#030947"

# -- Main Page Layout -- 

class Window():

    def __init__(self) -> None:

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QWidget()

        self.window.resize(1000,800)
        self.window.move(300,0)
        
        self.window.setWindowTitle('Western Tech Data Science Tool')
        self.window.setWindowIcon(QtGui.QIcon("img/wtLogo.png"))

        self.layout = QtWidgets.QHBoxLayout()
        self.data = DataEntryWidget()
        self.graph = GraphingWidget() 

        self.layout.addWidget(self.data)
        self.layout.addWidget(self.graph)

        self.window.setLayout(self.layout)
        self.window.show()
        sys.exit(self.app.exec())


# -- Graphing Widget --

class GraphingWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        #self.text = QtWidgets.QLabel("Graph Goes Here", alignment = QtCore.Qt.AlignCenter)

        self.series = QtCharts.QLineSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(10, 5)
        self.series.append(QtCore.QPointF(11, 1))
        self.series.append(QtCore.QPointF(13, 3))
        self.series.append(QtCore.QPointF(17, 6))
        self.series.append(QtCore.QPointF(18, 3))
        self.series.append(QtCore.QPointF(20, 2))

        self.chart = QtCharts.QChart()
        self.chart.legend()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Simple line chart example")

        self._chart_view = QtCharts.QChartView(self.chart)

        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.layout.addWidget(self._chart_view)
        self.setLayout(self.layout)



# -- Data Entry Widget -- 

class DataEntryWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.headerLabel =  QtWidgets.QLabel("Data Selection:" , alignment = QtCore.Qt.AlignCenter)

        self.selectionLabel = QtWidgets.QLabel("Select a Dataset from a File: (.csv, .tsv, or .xslx)", alignment = QtCore.Qt.AlignCenter)

        self.fileSelector = QtWidgets.QFileDialog(self)
        self.fileSelector.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.fileSelector.setNameFilter("(*.csv, *.tsv, *.xslx)")

        self.chartTypeLabel = QtWidgets.QLabel("Select Chart Type: ", alignment = QtCore.Qt.AlignCenter)

        self.chartType = QtWidgets.QComboBox().addItems(["Select Chart Type:", "Bar Chart", "Line Graph", "Scatter Plot", "Pie Chart", "Percentage Chart", "Temperature Graph"])

        self.xAxis = AxisLabeler("X-Axis", True)
        self.yAxis = AxisLabeler("Y-Axis", False)
        self.chartTitle = AxisLabeler("Chart Title", False)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.headerLabel)

        self.setLayout(self.layout)



class AxisLabeler(QtWidgets.QWidget):

    def __init__(self, axis_name: str, header_box: bool) -> None:
        super().__init__()

        self.label = QtWidgets.QLabel("Enter the " + axis_name + " Label Text" + " and Select the Data Header: "*int(header_box))

        self.textBox = QtWidgets.QInputDialog()
        self.textBox.setInputMode(QtWidgets.QInputDialog.TextInput)
        self.layout = QtWidgets.QHBoxLayout()
        self.header_box = header_box

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textBox)

        if(header_box):
            self.headerSelector = QtWidgets.QComboBox()
            self.layout.addWidget(self.headerSelector)

        self.setLayout(self.layout)

    def getAxisLabel(self) -> str:
        return self.textBox.getText()

    def getAxisDataHeader(self)-> str:
        if(not self.header_box):
            return "n/a"
        else:
            return self.headerSelector.currentText()

    def setAxisDataHeaders(self, headers: list):
        self.headerSelector.addItems(headers)


class SeriesSelector(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.numSeries = 1
        self.seriesDescriptors = [SeriesDescriptor(self.numSeries)]

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addItem(self.seriesDescriptors[-1])

        self.setLayout(self.layout)


class SeriesDescriptor(QtWidgets.QWidget):

    def __init__(self, seriesNum) -> None:
        super().__init__()

        self.label = QtWidgets.QLabel("Series " + str(seriesNum) +": ")
        self.nameInput = QtWidgets.QInputDialog()
        self.nameInput.setInputMode(QtWidgets.QInputDialog.TextInput)
        self.headerSelector = QtWidgets.QComboBox()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.nameInput)
        self.layout.addWidget(self.headerSelector)

        self.setLayout(self.layout)
            

if __name__ == "__main__":
    app = Window()
