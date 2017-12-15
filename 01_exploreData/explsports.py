from numpy import genfromtxt
import numpy as np
import pandas as pd
import os
import sys

class Sport:
    """
    This simple wrapper class is used for 
        (1)     getting an insight into the dataset linked below
        (2)     exporting data in a different format for spark (this is just 
                used as utility; the entire analysis could have been done in
                spark using python just as easily. 


    Dataset is used form:
 https://archive.ics.uci.edu/ml/datasets/Daily+and+Sports+Activities

    For being able to execute the script, generate a folder called 
    raw/sports/
    in this directory. Put the unzipped content of the dataset in there. 

    """

    def __init__(self, sizeLimit = 10000):
        """
        Load the data from disk into memory.

        """
        self.reloadData(sizeLimit)

    def exportToScript(self, outputTest = "out/test", outputTrain = "out/train"):
        """
        Export the data to specified paths.

        Randomized train and test splits, randomized order in export.

        Structure original data:
            (60, 9920, 45)
        Structure output data:
            outputTest:
                batch1 <- shape: [9920 / 30][46] containing
                          the activity identifier in the last column
                batch2
                 ...
                batch60  (in case all batches are loaded initially)

            outputTrain:
                batch1 <- shape: [9920 / 70][45]; original data.
                batch2
                 ...
                batch60  (in case all batches are loaded initially)


        :param outputTest:      output test directory. RELATIVE PATH.
                                Export is conducted via exportToScript.
        :param outputTrain:     output train directory. RELATIVE PATH.
                                Export is conducted via exportToScript.
        :return:                /
        """

        for id_batch, batch in enumerate(self.dataFlat):

            labels = self.labels[id_batch]


            # generate random permutation and sort the batch and its
            # identifier accordingly
            perm = np.random.permutation(batch.shape[0])
            sum1 = np.sum(batch)
            labels = labels[perm]
            batch  = batch[perm]
            sum2 = np.sum(batch)


            threshold = int(batch.shape[0] / 30)
            testDat  =  batch[:threshold]
            trainDat =  batch[threshold:]
            testLbl  = labels[:threshold]

            # expand the test set by the label in the last variable
            testDat  = np.hstack((testDat, testLbl[:,np.newaxis]))

            # write 'em away
            delim = " "
            np.savetxt(outputTest  + '/' + str(id_batch) + '.csv', testDat,  delimiter=delim)
            np.savetxt(outputTrain + '/' + str(id_batch) + '.csv', trainDat, delimiter=delim)


    def touch(name):
        """
        Static utility method for touching file.
        :param name
        :return:
        """
        try:
            file=open(name, 'a')
            file.close()
        except:
            print("An error occurred creating file " + name)
            sys.exit(0)


    def reloadData(self, sizeLimit):
        """
        Function for getting the data. Data is stored internally into self.dataFlat
        :sizeLimit:          the max amount of rows (entries) per time batch.
        """

        ### hardcoded dataset parameters / amount of values to be used
        amountSegs = 60 
        amountActs = 19
        amountPers = 8

        #self.data = np.empty([amountSegs, amountActs, amountPers, 124, 45])  #< can be used for storing
                                                                              #  in non-flattened way
        # Temp flattened data, initialized for efficiency reasons.
        tmpDat = np.empty([amountSegs, sizeLimit, 45])
        lblDat = np.empty([amountSegs, sizeLimit])          #< contains the label

        # there are 19 activities (19 folders)
        # desired output: for non-flattened
        # [Time identifier ^ segment] [activity ^ folder ] [person ^ folder] [sensor..sensor]
        path = "raw/sports"
        crows = np.zeros(amountSegs).astype(int) 


        for act_ident, act_path in enumerate(os.listdir(path)):
            newPath = path + str("/") + act_path
            if (False == os.path.isdir(newPath) or act_ident >= amountActs):
                print("break due to act"); break           #< threshold

            for pers_ident, pers_path in enumerate(os.listdir(newPath)):
                newestPath = newPath + str("/") +pers_path
                if (not os.path.isdir(newestPath) or (pers_ident >= amountPers)):
                    print("break due to pers"); break    #< threshold

                for seg_ident, seg_path in enumerate(os.listdir(newestPath)):
                    if (seg_ident >= amountSegs): print("break due to sek"); break; #< threshold
                    finalPath = newestPath + str("/") + seg_path

                    # fetch batch
                    batch = np.array(pd.read_csv(finalPath, delimiter=',',
                        quotechar='"', skipinitialspace=True))
                    if (crows[seg_ident] + batch.shape[0] > tmpDat.shape[1]):
                        print("passed max size (given as [default] parameter)"); break;
                    tmpDat[seg_ident, crows[seg_ident]:crows[seg_ident] + batch.shape[0]] = batch;
                    lblDat[seg_ident, crows[seg_ident]:crows[seg_ident] + batch.shape[0]] = seg_ident;
                    crows[seg_ident] += batch.shape[0]

                    # for non-flattened data
                    #self.data[seg_ident, act_ident, pers_ident, :, :] = batch;



        # remove the noise
        minval = np.min(crows)
        self.dataFlat = np.empty([amountSegs, minval, 45])
        self.labels   = np.empty([amountSegs, minval])
        for seg, crow in enumerate(crows):
            self.dataFlat[seg] = tmpDat[seg,0:minval]
            self.labels[seg] =   lblDat[seg,0:minval]



