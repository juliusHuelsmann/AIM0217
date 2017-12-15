from numpy import genfromtxt
import numpy as np

class DataAnalysis: 


    def __init__(self):

        # datetime,CellID,countrycode,smsin,smsout,callin,callout,internet
        self.SMS_IN  = 3
        self.SMS_OUT = 4
        self.CALL_IN = 5
        self.CALL_OUT= 6

        self.INTERNET= 7
        self.SMS     = 4
        self.CALL    = 6

        #self.reloadData(np.arange(1,2))
        self.reloadData()


    def reloadData(self, sets = np.arange(1,8)):
        """
        function for getting the smartphone data.
        """
        ### hardcoded dataset paths
        self.data = np.array([]) 
        prefix = "raw/mobile/sms-call-internet-mi-2013-11-0";
        postfix = ".csv"
        for i in sets:
            print(i)
            path = prefix + str(i) + postfix 
            batch = genfromtxt(path, delimiter=',')
            self.data = np.vstack((batch[1:], batch)) if self.data.shape[0] else batch





