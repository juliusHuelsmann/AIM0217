from numpy import genfromtxt
import numpy as np
import pandas as pd


class PowerConsumption:
    """
    https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption
    """

    def __init__(self):
        self.reloadData()


    def reloadData(self):
        """
        function for getting the smartphone data.
        """
        ### hardcoded dataset paths
        self.data = np.array([]) 
        paths = [
                "raw/power/household_power_consumption.txt"
                ]

        self.data = np.array([])
        for path in paths:
            batch = np.array(pd.read_csv(path, delimiter=';',
                    quotechar='"', skipinitialspace=True))
            self.data = np.vstack((batch[1:], batch)) if self.data.shape[0] else batch
            return;

#k = CrimesAnalysis()


