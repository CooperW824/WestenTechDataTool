
from fileinput import filename
import sys
from PySide6 import QtWidgets, QtGui, QtCore, QtCharts
from matplotlib.pyplot import axis
import dataset as ds

class Window():

    def __init__(self) -> None:

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QWidget()

        screenSize = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen())
        self.window.resize(screenSize.width(),int(screenSize.height()*0.97))
        self.window.move(0,0)
        
        self.window.setWindowTitle('Western Tech Data Science Tool')
        self.window.setWindowIcon(QtGui.QIcon("img/wtLogo.png"))

        self.mainComp = MainComponent()
        self.graphBtn = QtWidgets.QPushButton("Generate Graph")
        self.graphBtn.clicked.connect(self.graphData)
        self.graphBtn.setMaximumHeight(20)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.mainComp)
        self.layout.addWidget(self.graphBtn)

        self.window.setLayout(self.layout)
        self.window.setWindowState(QtGui.Qt.WindowMaximized)
        self.window.show()
        sys.exit(self.app.exec())

    @QtCore.Slot()
    def graphData(self):
        self.mainComp.graphData()

#--Main Component Class -- 

class MainComponent(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.data = DataEntryWidget()
        self.graph = GraphingWidget() 

        self.layout.addWidget(self.data)
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)

    def graphData(self):
        axisInfo = self.data.getAxesInfo()
        graphType = self.data.getGraphType()
        dataset = self.data.getDataset()

        x_data = dataset.getDataFromHeader(axisInfo[0][1])
        series_data = []
        for i in axisInfo[2]:
            series_data.append([dataset.getDataFromHeader(i[1]), i[0]])

        if graphType == "Line Graph":
            self.graph.buildLineChart(x_data, series_data)
            self.graph.setChartInfo(axisInfo[0][1], axisInfo[1], axisInfo[3])
        elif graphType == "Select Chart Type:":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please Select a Chart Type")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setWindowTitle("Max Number of Series Reached")
            msgBox.setWindowIcon(QtGui.QIcon("img/wtLogo.png"))
            msgBox.exec()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Sorry that graph type is not functional yet, but will be added very soon.")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setWindowTitle("Max Number of Series Reached")
            msgBox.setWindowIcon(QtGui.QIcon("img/wtLogo.png"))
            msgBox.exec()

            

# -- Graphing Widget --

class GraphingWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.chart = QtCharts.QChart()
        self.chart.legend()
        

        self._chart_view = QtCharts.QChartView(self.chart)

        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.layout.addWidget(self._chart_view)
        self.setLayout(self.layout)

    def buildLineChart(self, x_axes: list, y_axes: list):
        self.chart.removeAllSeries()

        for i in range(0, len(y_axes)):
            series = QtCharts.QLineSeries()
            series.setName(y_axes[i][1])
            for j in range(0, len(y_axes[i][0])):
                series.append(x_axes[j], y_axes[i][0][j])
            self.chart.addSeries(series)

        self.chart.createDefaultAxes()
        
        
    
    def setChartInfo(self, x_axis_title: str, y_axis_title: str, chart_title: str):
        self.chart.setTitle(chart_title)
        



# -- Data Entry Widget -- 

class DataEntryWidget(QtWidgets.QWidget):

    dataSet = None

    def __init__(self) -> None:
        super().__init__()

        self.headerLabel =  QtWidgets.QLabel("Data Selection:", alignment = QtCore.Qt.AlignCenter)
        self.headerLabel.setFixedHeight(20)

        self.selectionLabel = QtWidgets.QLabel("Select a Dataset from a File: (.csv, .tsv, or .xslx)", alignment = QtCore.Qt.AlignCenter)
        self.selectionLabel.setFixedHeight(20)

        self.fileSelectButton = QtWidgets.QPushButton("Select File")
        self.fileSelectButton.clicked.connect(self.selectFile)

        self.chartTypeLabel = QtWidgets.QLabel("Select Chart Type: ", alignment = QtCore.Qt.AlignCenter)
        self.chartTypeLabel.setFixedHeight(20)
        

        self.chartType = QtWidgets.QComboBox()
        self.chartType.addItems(["Select Chart Type:", "Bar Chart", "Line Graph", "Scatter Plot", "Pie Chart", "Percentage Chart", "Temperature Graph"])
        self.setFixedWidth(400)

        self.xAxis = AxisLabeler("X-Axis", True)
        self.yAxis = AxisLabeler("Y-Axis", False)
        self.yAxis.setMaximumHeight(60)
        self.chartTitle = AxisLabeler("Chart Title", False)
        self.chartTitle.setMaximumHeight(60)

        self.legend = SeriesSelector()

        self.addSeriesButton = QtWidgets.QPushButton("Add New Series")
        self.addSeriesButton.clicked.connect(self.legend.addSeriesDescriptor)

        self.regressionLabel = QtWidgets.QLabel("Regression Analysis (Line of Best Fit): \n(Warning: This is not implemented yet and does not work.)")
        self.regressionLabel.setFixedHeight(40)
        self.regressionSelector = QtWidgets.QComboBox()
        self.regressionSelector.addItems(["None", "Linear", "Quadratic", "Cubic", "Quartic", "Exponential", "Logistic", "Sinusoidal"])

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.selectionLabel)
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
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Dataset", filter="CSV (*.csv);;TSV (*.tsv);;Excel (*.xlsx)")
        self.dataSet = ds.Dataset(self.filepath[0])
        self.xAxis.setAxisDataHeaders(self.dataSet.getHeadersOfData())
        self.legend.setSeriesDescriptorsHeaders(self.dataSet)
        self.legend.dataset = self.dataSet
        filename = self.filepath[0]
        filename = filename.split("/")

        self.selectionLabel.setText("File: " + filename[-1])
        

    def getAxesInfo(self):  
        X_Axix = [self.xAxis.getAxisLabel(), self.xAxis.getAxisDataHeader()]
        Y_Axis = self.yAxis.getAxisLabel()
        numSeries = 1
        seriesInfo = []
        for i in self.legend.seriesDescriptors:
             seriesInfo.append([i.getAxisLabel(), i.getAxisDataHeader()])

        return X_Axix, Y_Axis, seriesInfo, self.chartTitle.getAxisLabel()
        
    def getDataset(self)-> ds.Dataset:
        return self.dataSet

    def getGraphType(self)->str:
        text = self.chartType.currentText()
        return text


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
        return self.textBox.text()

    def getAxisDataHeader(self)-> str:
        if(not self.header_box):
            return "n/a"
        else:
            return self.headerSelector.currentText()

    def setAxisDataHeaders(self, headers: list):
        self.headerSelector.addItems(headers)


class SeriesSelector(QtWidgets.QWidget):

    dataset = None

    def __init__(self) -> None:
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.numSeries = 1
        descriptor = SeriesDescriptor(self.numSeries)
        descriptor.setMaximumHeight(85)
        self.seriesDescriptors = [descriptor]
        
        self.layout.addWidget(self.seriesDescriptors[0])
        self.setLayout(self.layout)
       
    
    @QtCore.Slot()
    def addSeriesDescriptor(self):
        if self.numSeries < 3 and self.dataset != None:
            self.numSeries+=1
            descriptor = SeriesDescriptor(self.numSeries)
            descriptor.setMaximumHeight(85)
            self.seriesDescriptors.append(descriptor)
            descriptor.setAxisDataHeaders(self.dataset.getHeadersOfData())
            self.layout.addWidget(descriptor)
        else:
            msgBox = QtWidgets.QMessageBox()
            if self.numSeries > 2:
                msgBox.setText("You can only have up to 3 Series")
            else: 
                msgBox.setText("Please select a Dataset First")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setWindowTitle("Max Number of Series Reached")
            msgBox.setWindowIcon(QtGui.QIcon("img/wtLogo.png"))
            ret = msgBox.exec()

    def setSeriesDescriptorsHeaders(self, dataset:ds.Dataset):
        self.dataset = dataset
        headers = self.dataset.getHeadersOfData()
        for descriptor in self.seriesDescriptors:
            descriptor.setAxisDataHeaders(headers)


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
         return self.nameInput.text()

    def getAxisDataHeader(self)-> str:
        return self.headerSelector.currentText()

    def setAxisDataHeaders(self, headers: list) -> None:
        self.headerSelector.addItems(headers)
            
            
app = Window()

  
