

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.clustering import StreamingKMeans
from pyspark import SparkContext
from pyspark.streaming.context import StreamingContext
import numpy as np
from parser import ParserImpl
import os

class OperatorImpl:


    def __init__(self, model):

        # this file has to be cleared manually
        self.f_centers=open('../01_exploreData/out/check/centers.csv', 'wb')
        self.f_testRaw=open('../01_exploreData/out/check/testRaw.csv', 'wb')
        self.f_trainRaw=open('../01_exploreData/out/check/trainRaw.csv', 'wb')

        # contains the test - labels
        self.f_testLabels=open('../01_exploreData/out/check/testLabels.csv', 'wb')
        self.f_trainLabels=open('../01_exploreData/out/check/trainLabels.csv', 'wb')

        self.model = model

    def trainingHook(self, dateTime, nv):
        np.savetxt(self.f_trainRaw, nv.collect(), delimiter=",")
        return nv

    def trainResultHook(self, dateTime, nv):
        np.savetxt(self.f_trainLabels, nv.collect(), delimiter=",")
        return nv

    def testResultHook(self, dateTime, nv):
        #  write test labels
        np.savetxt(self.f_testLabels, nv.collect(), delimiter=",")

        # write centers
        newValues = self.model.latestModel().centers
        ParserImpl.mats = np.hstack((ParserImpl.mats, newValues[np.newaxis,:])) if  ParserImpl.mats.shape[0] else newValues[np.newaxis,:]
        np.savetxt(self.f_centers, newValues, delimiter=",")
        return nv


    def testingHook(self, dateTime, nv):

        # save raw data
        li = []
        k = nv.collect()
        for i, el in enumerate(k):
            li.append(el.features)

        np.savetxt(self.f_testRaw, np.array(li), delimiter="," )
        return nv

    def close(self):
        try:
            self.f_testRaw.close()
            self.f_centers.close()
            self.f_trainRaw.close()
            self.f_testLabels.close()
            self.f_trainLabels.close()
        except:
            pass


