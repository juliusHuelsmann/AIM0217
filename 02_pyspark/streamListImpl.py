#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pyspark.streaming.listener import StreamingListener

class StreamingListenerImpl(StreamingListener):

    def __init__(self, testLabels, testRaw, trainRaw, centers):
        StreamingListener.__init__(self)
        self.testLabels = testLabels
        self.testRaw = testRaw
        self.trainRaw = trainRaw
        self.centers = centers
        pass

    def onReceiverStarted(self, receiverStarted):
        """
        Called when a receiver has been started
        """
    pass


    def onReceiverError(self, receiverError):
        """
        Called when a receiver has reported an error
        """
    pass


    def onReceiverStopped(self, receiverStopped):
        """
        Called when a receiver has been stopped
        """
    pass


    def onBatchSubmitted(self, batchSubmitted):
        #print("Batch submitted!")
        """
        Called when a batch of jobs has been submitted for processing.
        """
        pass


    def onBatchStarted(self, batchStarted):
        print("Batch started!")
        self.testLabels.write("Batch started!\n")
        self.testRaw.write("Batch started!\n")
        self.trainRaw.write("Batch started!\n")
        self.centers.write("Batch started!\n")
        #print("j", batchStarted.batchInfo().numRecords())
        """
        Called when processing of a batch of jobs has started.
        """
        #print("Batch started!")
        self.testRes.write("Batch started!\n")
        #print("j", batchStarted.batchInfo().numRecords())
        return 0

    def onBatchCompleted(self, batchCompleted):
        print("Batch completed!")
        self.testLabels.write("Batch completed!\n")
        self.testRaw.write("Batch completed!\n")
        self.trainRaw.write("Batch completed!\n")
        self.centers.write("Batch completed!\n")
        #print("k", batchCompleted.batchInfo().numRecords())
        """
        Called when processing of a batch of jobs has completed.
        """
        pass


    def onOutputOperationStarted(self, outputOperationStarted):
        """
        Called when processing of a job of a batch has started.
        """
    pass


    def onOutputOperationCompleted(self, outputOperationCompleted):
        """
        Called when processing of a job of a batch has completed
        """
    pass
