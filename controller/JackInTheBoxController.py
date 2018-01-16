#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math

import os
pathInterface = os.path.dirname(os.path.abspath(__file__))+'/../arduino/JackInTheBox/'
pathController = os.path.dirname(os.path.abspath(__file__))+'/../controller/camshare/'


####### For cable calibration
# disable 9
# crtl + cableId (0 1 2 3 4 5 6 7)
# ctrl + "+"
# ctrl + "-"
# ctrl + "*" to save


def normalize(x):
    norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
    for i in range(0,3):
        x[i] = x[i]/norm


def readOffset():
    offsetList = [0.]*11
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
    for i in range(0,11):
        offsetStr +=" "+str(offsetList[i])
    print "saved offset = "+offsetStr

    offsetFile.write(offsetStr)
    offsetFile.close()


def readFromMotionCapture():
    nbPoint = 4
    positionsList = [0.]*3*nbPoint
    positionsFile = open(pathController+"zzkcurrent.txt","r")
    i=0
    for line in positionsFile:
        for position in line.split():
                positionsList[i] = float(position)
                i+=1
    positionsFile.close()
    return positionsList


#Takes a 3d vector and normalize it
def normalizeQuat(x):
    norm = numpy.sqrt(x[3]*x[3] + x[4]*x[4] + x[5]*x[5] + x[6]*x[6])
    for i in range(3,7):
        x[i] = x[i]/norm
    return x


class controller(Sofa.PythonScriptController):

    def initGraph(self, node):
            self.node = node

            self.openingMO = node.getChild('opening').getObject('MO')
            self.manivelleMO = node.getChild('manivelle').getObject('MO')

            self.rotation = 73
            self.openingInitialAngle = 0.06
            self.initOpening()

            #Offset for cable calibration
            self.offsetList = readOffset()
            self.cableId = 0
            self.doChangeOffset = 0

            self.sendDisplacementsToSerial()


    def bwdInitGraph(self, node):
            self.sendDisplacementsToSerial()


    def onBeginAnimationStep(self,dt):
        self.updateCableLimits()
        self.getRotationFromPotentiometer()
        #self.getMappingFromMotionCapture()
        self.translateGoal()



    def onEndAnimationStep(self,dt):
        self.sendDisplacementsToSerial()



    def getRotationFromPotentiometer(self):
        receivedData = self.node.getObject('serial').findData('receivedData').value

        if receivedData[0][0] > 0:
            self.rotation = receivedData[0][0]
            #print self.rotation

        positionOpening = self.openingMO.findData("position").value
        positionOpening[0][3]= (73-self.rotation)*0.008 - self.openingInitialAngle
        self.openingMO.findData("position").value = positionOpening



    def initOpening(self):
        positionOpening = self.openingMO.findData("position").value
        positionOpening[0][3]=-self.openingInitialAngle #40°

        self.openingMO.findData("position").value = positionOpening


    def getMappingFromMotionCapture(self):

        MCPositions = readFromMotionCapture()

        footPositions = [0, -80, 0]
        distances = [69, 130, 116.2, 116.2, 150]

        hipFromMC  = [MCPositions[0],MCPositions[1],-MCPositions[2]]
        handLFromMC  = [MCPositions[3],MCPositions[4],-MCPositions[5]]
        handRFromMC = [MCPositions[6],MCPositions[7],-MCPositions[8]]
        headFromMC = [MCPositions[9],MCPositions[10],-MCPositions[11]]

        #On fixe le bassin dans le plan (z,y)
        hipDirection = hipFromMC
        normalize(hipDirection)

        hip1 = [0, footPositions[1]+hipDirection[1]*distances[0], footPositions[2]+hipDirection[2]*distances[0]]
        hip2 = [0, footPositions[1]+hipDirection[1]*distances[1], footPositions[2]+hipDirection[2]*distances[1]]

        #Pour les mains et la tete on fixe aussi les distances
        #et on prend les direction par rapport aux hanches

        hipFromMC = [MCPositions[0],MCPositions[1],-MCPositions[2]]

        handLDirecion = [handLFromMC[0]-hipFromMC[0], handLFromMC[1]-hipFromMC[1], handLFromMC[2]-hipFromMC[2]]
        handRDirecion = [handRFromMC[0]-hipFromMC[0], handRFromMC[1]-hipFromMC[1], handRFromMC[2]-hipFromMC[2]]
        headDirecion  = [headFromMC[0]-hipFromMC[0],  headFromMC[1]-hipFromMC[1],  headFromMC[2]-hipFromMC[2]]

        normalize(handLDirecion)
        normalize(handRDirecion)
        normalize(headDirecion)

        handL = [hip2[0]+handLDirecion[0]*distances[2], hip2[1]+handLDirecion[1]*distances[2], hip2[2]+handLDirecion[2]*distances[2]]
        handR = [hip2[0]+handRDirecion[0]*distances[3], hip2[1]+handRDirecion[1]*distances[3], hip2[2]+handRDirecion[2]*distances[3]]
        head  = [hip2[0]+headDirecion[0]*distances[4],  hip2[1]+headDirecion[1]*distances[4],  hip2[2]+headDirecion[2]*distances[4]]

        positions = [hip1, hip2, handL, handR, head]
        #print positions

        backup = self.node.getChild("goal").getObject("goalMO").findData("position").value
        if(math.isnan(hip1[0]) or math.isnan(hip1[1]) or math.isnan(hip1[2]) or math.isnan(handL[0]) or math.isnan(handL[1]) or math.isnan(handL[2])
        or math.isnan(handR[0]) or math.isnan(handR[1]) or math.isnan(handR[2]) or math.isnan(head[0]) or math.isnan(head[1]) or math.isnan(head[2])):
            positions = backup

        self.node.getChild("goal").getObject("goalMO").findData("position").value = positions



    def translateGoal(self):
        positions = self.node.getChild("goalVisuInteraction").getObject("goalMO").findData("position").value
        positions[0][0] -= 50
        positions[1][0] -= 50
        positions[4][0] -= 50
        self.node.getChild("goal").getObject("goalMO").findData("position").value = positions



    def sendDisplacementsToSerial(self):

        displacements = [0.0]*11
        for i in range(0,11):
            displacements[i] = self.node.getChild('accordion').getChild('cable'+str(i+1)).getObject("cable").findData('displacement').value

        pressures = [0.0]*3
        for i in range(0,3):
            pressures[i] = self.node.getChild('accordion').getChild('cavity'+str(i+1)).getObject("pressure").findData('pressure').value

        outputVector = [
        displacements[0] + self.offsetList[0],
        displacements[1] + self.offsetList[1],
        displacements[2] + self.offsetList[2],
        displacements[3] + self.offsetList[3],
        displacements[4] + self.offsetList[4],
        displacements[5] + self.offsetList[5],
        displacements[7] + self.offsetList[7],
        displacements[6] + self.offsetList[6],
        displacements[9] + self.offsetList[9],
        displacements[8] + self.offsetList[8],
        displacements[10] + self.offsetList[10],
        pressures[2]*10+8,
        pressures[1]*10+7,
        pressures[0]*10+6
        ]

        for i in range(0,11):
            outputVector[i] = 125*outputVector[i]/65 + 125
            if outputVector[i] > 250:
                outputVector[i] = 250

            if outputVector[i] < 0:
                outputVector[i] = 0

        for i in range(11,14):
            if outputVector[i]> 11:
                outputVector[i]= 11

        self.node.getObject('serial').findData('sentData').value = outputVector


    def updateCableLimits(self):
        ##Update cable limits per section

        cable1 = self.node.getChild('accordion').getChild('cable1').getObject('cable').findData('displacement').value
        cable2 = self.node.getChild('accordion').getChild('cable2').getObject('cable').findData('displacement').value
        cable3 = self.node.getChild('accordion').getChild('cable3').getObject('cable').findData('displacement').value

        cable4 = self.node.getChild('accordion').getChild('cable4').getObject('cable').findData('displacement').value
        cable6 = self.node.getChild('accordion').getChild('cable6').getObject('cable').findData('displacement').value

        self.maxPositiveDisp = 40

        if cable1>0:
            self.node.getChild('accordion').getChild('cable4').getObject('cable').findData('maxPositiveDisp').value = self.maxPositiveDisp + cable1
        if cable2>0:
            self.node.getChild('accordion').getChild('cable5').getObject('cable').findData('maxPositiveDisp').value = self.maxPositiveDisp + cable2
        if cable3>0:
            self.node.getChild('accordion').getChild('cable6').getObject('cable').findData('maxPositiveDisp').value = self.maxPositiveDisp + cable3

        if cable4>0:
            self.node.getChild('accordion').getChild('cable7').getObject('cable').findData('maxPositiveDisp').value = self.maxPositiveDisp + cable4
        if cable6>0:
            self.node.getChild('accordion').getChild('cable8').getObject('cable').findData('maxPositiveDisp').value = self.maxPositiveDisp + cable6

        self.node.getChild('accordion').getChild('cable4').getObject('cable').reinit()
        self.node.getChild('accordion').getChild('cable5').getObject('cable').reinit()
        self.node.getChild('accordion').getChild('cable6').getObject('cable').reinit()
        self.node.getChild('accordion').getChild('cable7').getObject('cable').reinit()
        self.node.getChild('accordion').getChild('cable8').getObject('cable').reinit()



    def onKeyPressed(self,c):
        if(c=="9"):
            self.doChangeOffset = not self.doChangeOffset
            print "Change offset active: "+str(self.doChangeOffset)


        ##Control cables
        ##8 cables

        ##Choose cable
        if(self.doChangeOffset):
            for i in range(0,10):
                if(c==str(i)):
                    self.cableId = i
                    print "Controlled cable ID: "+str(self.cableId)

            #Actuate cable
            if(c=="+"):
                self.offsetList[self.cableId]+=1
                print self.offsetList
            if(c=="-"):
                self.offsetList[self.cableId]-=1
                print self.offsetList

            if(c=="*"):
                writeOffset(self.offsetList)
        else:
            #Actuate opening
            if(c=="+"):
                self.openingInitialAngle+=0.01
            if(c=="-"):
                self.openingInitialAngle-=0.01
