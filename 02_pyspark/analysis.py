import numpy as np
import pandas as pd

import matplotlib.pyplot as plt



amountBatches = 60
amountClusters = 3
dim = 45


def loadCenter(amountClusters, path="../01_exploreData/out/check/centers.csv" ):
    """
    Load the center
    
    """
    
    print(path)
    

    # fetch the batch
    batch = np.array(np.loadtxt(path, delimiter=','))
   
    val = batch[0:60*amountClusters]
    print("hier", batch.shape, val.shape, "amountclusters", amountClusters)
    
    batch = batch[:amountClusters*60,:] #< discard batchest that are non-existent. 
    batch = batch.reshape([int(batch.shape[0]/amountClusters), amountClusters, batch.shape[1]])

    # u never know unless u think! or insert assertions!
    #assert((val[0] == batch[0,0]).all())
    #assert((val[1] == batch[0,1]).all())
    #assert((val[2] == batch[0,2]).all())
    #assert((val[3] == batch[1,0]).all())

    return batch

def loadFeatures(path="../01_exploreData/out/check/testRaw.csv"):
    # fetch the batch
    batch = np.array(np.loadtxt(path, delimiter=','))
    line_per_batch = int(batch.shape[0] / amountBatches)
    print(line_per_batch)
    print(batch.shape)
    if (len(batch.shape) > 1):
        batch = batch.reshape([amountBatches, line_per_batch, batch.shape[1]])
    else:
        batch = batch.reshape([amountBatches, line_per_batch, 1])
    return batch


def getObjective(t, features, labels, centers):
    """
    :features:   The feature vector of dimensionality [times x linesPerTime x Dim=45]
    :labels:   The feature vector of dimensionality   [times x linesPerTime]
    """
    
    features = features[t]
    labels = labels[t]
    centers = centers[t]
    
    means = [centers[l] for l in labels.astype(int)]
    obj = np.linalg.norm(means - features) / labels.shape[0]
    return obj

def getWorst(t, features, labels, centers):
    """
    :features:   The feature vector of dimensionality [times x linesPerTime x Dim=45]
    :labels:   The feature vector of dimensionality   [times x linesPerTime]
    """
    
    features = features[t]
    labels = labels[t]
    centers = centers[t]
    
    means = np.mean(features)
    obj = np.linalg.norm(means - features) / labels.shape[0]
    return obj

colors = {0:"red", 1:"green", 2:"blue"}
colors = np.array(["red", "green", "blue"])
def plotPerDimension(features, labels, centers, timeUnit=0):
    """
    :timeUnit:   Time Unit that is selected for the plot
    :features:   The feature vector of dimensionality [times x linesPerTime x Dim=45]
    :labels:   The feature vector of dimensionality   [times x linesPerTime]
    """
    plt.figure(figsize=(100,100))
    
    # only get the current timeUnit
    features = features[timeUnit]
    labels = labels[timeUnit].astype(int)
    centers = centers[timeUnit]

    #labels = np.dot(labels[:,np.newaxis], np.array([.3, .3, .3])[np.newaxis,:])
    for dim1 in np.arange(features.shape[1]):
        
        print(dim1)
        for dim2 in np.arange(dim1, features.shape[1]):
            plt.subplot(features.shape[1], features.shape[1], dim1 * features.shape[1] + dim2 + 1)
            ## Plot centers
            
            plt.scatter(features[:,dim1], features[:,dim2], color=[colors[i] for i in labels], s=.2) # 
            plt.scatter(centers[:,dim1], centers[:,dim2], color=[colors[i] for i in range(centers.shape[0])], s=10, marker="x")



def getData(amountClusters, bulkExec="", timeUnitMax=10):
    """
    :bulkExex:   Identifier for the bulk execution. leave empty in case of normal execution.
    """
    center = loadCenter(amountClusters, path="../01_exploreData/out/check/" + bulkExec + "centers.csv" )
    testFeatures = loadFeatures("../01_exploreData/out/check/" + bulkExec + "testRaw.csv")
    trainFeatures = loadFeatures("../01_exploreData/out/check/" + bulkExec + "trainRaw.csv")
    testLabels = loadFeatures("../01_exploreData/out/check/" + bulkExec + "testLabels.csv")
    testLabels = testLabels[:,:,1]
    trainLabels = loadFeatures("../01_exploreData/out/check/" + bulkExec + "trainLabels.csv")
    
    #center = center[:timeUnitMax]
    testFeatures = testFeatures[:timeUnitMax]
    trainFeatures = trainFeatures[:timeUnitMax]
    testLabels = testLabels[:timeUnitMax]
    trainLabels = trainLabels[:timeUnitMax]
    
    print(testFeatures.shape, trainFeatures.shape)
    print(testLabels.shape, trainLabels.shape)
    features = np.empty([timeUnitMax, testFeatures.shape[1] + trainFeatures.shape[1], testFeatures.shape[2]])
    labels = np.empty([timeUnitMax, testLabels.shape[1] + trainLabels.shape[1], 1])
    for t in range(timeUnitMax):
        i = t
        features[t] = np.vstack((testFeatures[i], trainFeatures[i]))
        print(testLabels[i].shape, trainLabels[i,:,0].shape, labels[t].shape)
        labels[t] = np.vstack((testLabels[i][:,np.newaxis], trainLabels[i]))
    
    return testFeatures, trainFeatures, testLabels, trainLabels, features, labels, center
    
    
def getBulkObjective(bulkCount=10, amountBatches=5):
    """
    Returns objective function for bulk execution. 
    :bulkCount:   the amount of temporal batches to be processed.
    :return:      
    """
    
    js = np.empty([bulkCount, amountBatches])
    
    for k in np.arange(1, bulkCount+1):
        print("k = ", k)
        _, _, _, _, features, labels, centers= getData(k, "bulk" + str(k) + "/", timeUnitMax=amountBatches)
        
        js[k-1,:] = np.array([ getObjective(t, features, labels, centers) for t in np.arange(amountBatches)])

        #js[k-1,:] = np.array([ getObjective(t, testFeatures, testLabels, centers) for t in np.arange(amountBatches)])

buuu = getBulkObjective()



plt.figure()
plt.plot(buuu[:,0], buuu[:,1])
plt.savefig("hier.png")


