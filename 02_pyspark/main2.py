
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.clustering import StreamingKMeans
from pyspark import SparkContext
from pyspark.streaming.context import StreamingContext
import numpy as np
import os

# own impl
from streamListImpl import StreamingListenerImpl
from parser import ParserImpl
from operatorImpl import OperatorImpl

import sys


if __name__ == "__main__":

    
    # parameter parsing
    amountClusters = 3
    if (len(sys.argv) >= 2):
        amountClusters = int(sys.argv[1])
        print("loaded amount of cluster  = ", amountClusters, ".")
    else:
        print("launched with default amount of clusters k = ", amountClusters, ".")

    # Spark Context is running locally. creates a java Spark Context using Py4J
    # is attached to the local FS.
    # Data is stored as Picled (serializer) objects in RDD[Array[Byte]]
    sc  = SparkContext("local[*]", "localKMeans", pyFiles=[])
    ssc = StreamingContext(sc, batchDuration=1)
    sc.setLogLevel("INFO")

    # Load test and train files directly from python script output.
    # In case no data can be found, have a look at 
    # 01/exporeData/explsports.py or -- for a guided generation --
    # execute the jupyter notebook file Sports[...].ipynb, that can be 
    # found in the same directory.
    parser = ParserImpl()
    trainingStream, testingStream = parser.getTrainTestQueue(ssc, sc)

    # we create a model with random clusters and specify the number of clusters 
    # to find timeUnit = batches is the correct choice for the problem we 
    #  are currently investigating
    model = StreamingKMeans(k=amountClusters, decayFactor=0.5, timeUnit="batches")
    .setRandomCenters(45, 1.0, 0) #< dim, weight, seed
    modelOut = open( "../01_exploreData/out/check/models.txt", "w" )
    operator = OperatorImpl(model) #< contains our implementation of 
                                   #  specific operators for
                                   #  debugging and parameter tuning.

    # a streaming listerner that may be commented in for debugging.
    debug = 0
    if debug:
        k = StreamingListenerImpl(operator.f_testLabels, operator.f_testRaw, operator.f_trainRaw, operator.f_centers)
        ssc.addStreamingListener(k)

    trainingStream.foreachRDD(operator.trainingHook)
    testingStream.foreachRDD(operator.testingHook)
    model.trainOn(trainingStream)
    model.predictOnValues(testingStream.map(lambda lp: (lp.label, lp.features))).foreachRDD(operator.testResultHook)
    model.predictOn(trainingStream).foreachRDD(operator.trainResultHook)

    # start, stop and print for convenience ;-)
    ssc.start()
    ssc.awaitTermination(timeout=200)
    operator.close()
    print("Final centers: " + str(model.latestModel().centers))

