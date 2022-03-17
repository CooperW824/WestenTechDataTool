
import pandas as pd
import scipy as sp

class Dataset: 
    
    def __init__(self, pathToDataset: str) -> None:

        self._data = None
        path  = pathToDataset.split(".")
        type = path[-1]

        if type == "csv":
            self._data = pd.read_csv(pathToDataset)
        elif type == "tsv":
            self._data = pd.read_csv(pathToDataset, sep="\t")
        elif type == "xlsx":
            self._data = pd.read_excel(pathToDataset)
        else:
            raise TypeError("Invalid Dataset Type")

    def getHeadersOfData(self):
       return list(self._data.columns)

    def getDataFromHeader(self, column):
        return list(self._data[column])

    
