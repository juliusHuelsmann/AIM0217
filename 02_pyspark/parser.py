from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
import numpy as np
import os

class ParserImpl:
    """
    Custom parser class that is used for our input data.
    """

    def __init__(self):
        print("Parser initialized")
        ParserImpl.tuplesProcessed = ParserImpl.tuplesProcessed if ParserImpl.tuplesProcessed else 0
        self.debug = 0
        #self.debug = 1

    def parseTrainingData(self, lp):
        """
        Load training Data from file

        :param lp:      the line containing the data points
        :return:        a labeled point.
        """
        data = Vectors.dense(lp.strip().split(' '))
        ParserImpl.tuplesProcessed += 1

        if self.debug:
            if (self.tuplesProcessed >= 9590): #< amount for each file
                print("train passed", self.tuplesProcessed)

        #if (data.shape[0] == 45): exit(1)

        #label = float(lp[lp.find('(') + 1: lp.find(')')])
        #vec = Vectors.dense(lp[lp.find('[') + 1: lp.find(']')].split(','))


        return data

    def parseTestingData(self, lp):
        """
        In the training output file, the label is found in the last column

        :param lp:      the line containing the data points
        :return:        a labeled point.
        """
        data = Vectors.dense(lp.strip().split(' '))
        ParserImpl.tuplesProcessed += 1

        if self.debug:
            if (self.tuplesProcessed >= 330): #< amount for each file
                print("test passed" , self.tuplesProcessed)


        vec = data[:-1]
        label = data[-1]

        return LabeledPoint(label, vec)

    def getTrainTestQueue(self, ssc, sc):
        #
        # Queue of RDDs as a Stream:
        # For testing a Spark Streaming application with test data,
        # one can also create a DStream based on a queue of RDDs,
        # using streamingContext.queueStream(queueOfRDDs).
        # Each RDD pushed into the queue will be treated as a
        # batch of data in the DStream, and processed like a stream.
        #
        #trainingData = sc.textFile("../01_exploreData/out/train/*.csv").map(parser.parseTrainingData)
        #testingData  = sc.textFile("../01_exploreData/out/test/*.csv").map(parser.parseTestingData)

        #trainingQueue = [trainingData]
        #testingQueue =  [testingData]

        def get_sorted_filenames(foldername, fileending):
            files = [f for f in os.listdir(foldername) if f.endswith(fileending)]
            files = sorted(files,key=lambda x: int(os.path.splitext(x)[0]))
            files = [os.path.join(foldername, f) for f in files]
            return files

        trainingQueue=[]
        testingQueue=[]

        trainingfiles = get_sorted_filenames("../01_exploreData/out/train/", ".csv")
        testingfiles = get_sorted_filenames("../01_exploreData/out/test/", ".csv")

        for f_centers in trainingfiles:
            trainingQueue.append(sc.textFile(f_centers).map(self.parseTrainingData))
        for f_centers in testingfiles:
            testingQueue.append(sc.textFile(f_centers).map(self.parseTestingData))
        trainingStream = ssc.queueStream(trainingQueue)
        testingStream  = ssc.queueStream(testingQueue)
        return trainingStream, testingStream;


ParserImpl.tuplesProcessed = 0
ParserImpl.mats = np.array([])

