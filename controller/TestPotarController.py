#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa

import os
pathInterface = os.path.dirname(os.path.abspath(__file__))+'/../arduino/JackInTheBox/'


####### For cable calibration
# disable 9
# crtl + cableId (0 1 2 3 4 5 6 7)
# ctrl + "+"
# ctrl + "-"
# ctrl + "*" to save

def readOffset():
    offsetList = [0.]*10
    offsetFile = open(pathInterface+"offset.txt","r+")
    offsetStr = ""
    i=0
    for line in offsetFile:
        for offset in line.split():
                offsetList[i] = float(offset)
                offsetStr +=" "+str(offsetList[i])
                i+=1
    print "offset = "+offsetStr
    offsetFile.close()

    return offsetList

def writeOffset(offsetList):
    offsetFile = open(pathInterface+"offset.txt","r+")
    offsetStr = ""
    for i in range(0,10):
        offsetStr +=" "+str(offsetList[i])
    print "saved offset = "+offsetStr

    offsetFile.write(offsetStr)
    offsetFile.close()


class controller(Sofa.PythonScriptController):

    def initGraph(self, node):
            self.node = node

            self.openingMO = node.getChild('opening').getObject('MO')

            self.rotation = 73
            self.openingInitialAngle = 0.33
            self.initOpening()

            #Offset for cable calibration
            self.offsetList = readOffset()
            self.cableId = 0
            self.doChangeOffset = 0

            self.sendDisplacementsToSerial()


    def bwdInitGraph(self, node):
            self.sendDisplacementsToSerial()


    def onBeginAnimationStep(self,dt):
        self.getRotationFromPotentiometer()



    def onEndAnimationStep(self,dt):
        self.sendDisplacementsToSerial()



    def getRotationFromPotentiometer(self):
        receivedData = self.node.getObject('serial').findData('receivedData').value

        if receivedData[0][0] > 0:
            self.rotation = receivedData[0][0]
            print self.rotation
        else:
            print "fuck" + str(receivedData[0][0])

        positionOpening = self.openingMO.findData("position").value
        positionOpening[0][3]= (73-self.rotation)*0.008 - self.openingInitialAngle
        self.openingMO.findData("position").value = positionOpening



    def initOpening(self):
        positionOpening = self.openingMO.findData("position").value
        positionOpening[0][3]=-self.openingInitialAngle #40°

        self.openingMO.findData("position").value = positionOpening



    def sendDisplacementsToSerial(self):


        outputVector = [
        self.offsetList[0],
        self.offsetList[1],
        self.offsetList[2],
        self.offsetList[3],
        self.offsetList[4],
        self.offsetList[5],
        self.offsetList[6],
        self.offsetList[7],
        self.offsetList[8],
        self.offsetList[9],
        5,
        5,
        5
        ]

        for i in range(0,10):
            outputVector[i] = 127*outputVector[i]/75 + 127
            if outputVector[i] > 255:
                outputVector[i] = 255
            if outputVector[i] < 0:
                outputVector[i] = 0

        #print outputVector
        self.node.getObject('serial').findData('sentData').value = outputVector
