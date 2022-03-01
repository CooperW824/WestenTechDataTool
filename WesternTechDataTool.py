
import sys
from PySide6 import QtWidgets, QtGui, QtCore, QtCharts
from PySide6.QtCore import Signal


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

        screenSize = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen())
        self.window.resize(screenSize.width(),int(screenSize.height()*0.97))
        self.window.move(0,0)
        
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

        self.headerLabel =  QtWidgets.QLabel("Data Selection:", alignment = QtCore.Qt.AlignCenter)
        self.headerLabel.setFixedHeight(20)

        self.selectionLabel = QtWidgets.QLabel("Select a Dataset from a File: (.csv, .tsv, or .xslx)", alignment = QtCore.Qt.AlignCenter)
        self.selectionLabel.setFixedHeight(20)

        self.fileSelectButton = QtWidgets.QPushButton("Select File")

        self.fileSelector = QtWidgets.QFileDialog(self)
        self.fileSelector.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.fileSelector.setNameFilter("(*.csv, *.tsv, *.xslx)")

        self.fileSelectButton.clicked.connect(self.selectFile)

        self.chartTypeLabel = QtWidgets.QLabel("Select Chart Type: ", alignment = QtCore.Qt.AlignCenter)
        self.chartTypeLabel.setFixedHeight(20)
        

        self.chartType = QtWidgets.QComboBox()
        self.chartType.addItems(["Select Chart Type:", "Bar Chart", "Line Graph", "Scatter Plot", "Pie Chart", "Percentage Chart", "Temperature Graph"])
        self.setFixedWidth(400)

        self.xAxis = AxisLabeler("X-Axis", True)
        self.yAxis = AxisLabeler("Y-Axis", False)
        self.chartTitle = AxisLabeler("Chart Title", False)

        self.legend = SeriesSelector()

        self.addSeriesButton = QtWidgets.QPushButton("Add New Series")
        self.addSeriesButton.clicked.connect(self.legend.addSeriesDescriptor)

        self.regressionLabel = QtWidgets.QLabel("Regression Analysis (Line of Best Fit):")
        self.regressionLabel.setFixedHeight(20)
        self.regressionSelector = QtWidgets.QComboBox()
        self.regressionSelector.addItems(["None", "Linear", "Quadratic", "Cubic", "Quartic", "Exponential", "Logistic", "Sinusoidal"])
        
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.headerLabel)

        self.layout.addWidget(self.selectionLabel)
        self.layout.addWidget(self.fileSelector)
        self.layout.addWidget(self.fileSelectButton)
        self.layout.addWidget(self.chartTypeLabel)
        self.layout.addWidget(self.chartType)
        self.layout.addWidget(self.xAxis)
        self.layout.addWidget(self.yAxis)
        self.layout.addWidget(self.chartTitle)
        self.layout.addWidget(self.legend)
        self.layout.addWidget(self.addSeriesButton)
        self.layout.addWidget(self.regressionLabel)
        self.layout.addWidget(self.regressionSelector)


        self.setLayout(self.layout)

        self.scroll = QtWidgets.QScrollArea()
        #Scroll Area Properties
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)

        


    @QtCore.Slot()
    def selectFile(self):
        self.fileSelector.open()




class AxisLabeler(QtWidgets.QWidget):

    def __init__(self, axis_name: str, header_box: bool) -> None:
        super().__init__()

        self.setMaximumHeight(60)

        self.label = QtWidgets.QLabel("Enter the " + axis_name + " Label Text" + " and Select the Data Header: "*int(header_box))
        self.label.setMaximumHeight(30)

        self.textBox = QtWidgets.QLineEdit()

        self.layout = QtWidgets.QVBoxLayout()
        self.header_box = header_box

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textBox)

        if(header_box):
            self.headerSelector = QtWidgets.QComboBox()
            self.layout.addWidget(self.headerSelector)
            self.setMaximumHeight(85)

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

        self.layout = QtWidgets.QVBoxLayout()
        self.numSeries = 1
        self.seriesDescriptors = [SeriesDescriptor(self.numSeries)]
        
        self.layout.addWidget(self.seriesDescriptors[0])
        self.setLayout(self.layout)
       
    
    @QtCore.Slot()
    def addSeriesDescriptor(self):
        self.numSeries+=1
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("You can only have up to 3 Series")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setWindowTitle("Max Number of Series Reached")
        msgBox.setWindowIcon(QtGui.QIcon("img/wtLogo.png"))
        if self.numSeries < 4:
            descriptor = SeriesDescriptor(self.numSeries)
            self.seriesDescriptors.append(descriptor)
            self.layout.addWidget(descriptor)
        else:
            
            ret = msgBox.exec()

        


class SeriesDescriptor(QtWidgets.QWidget):

    def __init__(self, seriesNum) -> None:
        super().__init__()

        self.label = QtWidgets.QLabel("Series " + str(seriesNum) +": ")
        self.label.setMaximumHeight(30)
        self.nameInput = QtWidgets.QLineEdit()
        self.headerSelector = QtWidgets.QComboBox()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.nameInput)
        self.layout.addWidget(self.headerSelector)

        self.setLayout(self.layout)

    def getAxisLabel(self) -> str:
        return self.nameInput.getText()

    def getAxisDataHeader(self)-> str:
        return self.headerSelector.currentText()

    def setAxisDataHeaders(self, headers: list) -> None:
        self.headerSelector.addItems(headers)
            

if __name__ == "__main__":
    app = Window()
