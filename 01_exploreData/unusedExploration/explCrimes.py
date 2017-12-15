from numpy import genfromtxt
import numpy as np
import pandas as pd


class CrimesAnalysis: 


    def __init__(self):
        self.reloadData()


    def reloadData(self):
        """
        function for getting the smartphone data.
        """
        ### hardcoded dataset paths
        self.data = np.array([]) 
        paths = [
                "raw/crimes/Chicago_Crimes_2001_to_2004.csv",
                "raw/crimes/Chicago_Crimes_2005_to_2007.csv",
                "raw/crimes/Chicago_Crimes_2008_to_2011.csv",
                "raw/crimes/Chicago_Crimes_2012_to_2017.csv"
                ]
        self.data = np.array([])
        for path in paths:
            batch = np.array(pd.read_csv(path, delimiter=',',
                    quotechar='"', skipinitialspace=True))
            self.data = np.vstack((batch[1:], batch)) if self.data.shape[0] else batch
            return;

#k = CrimesAnalysis()


