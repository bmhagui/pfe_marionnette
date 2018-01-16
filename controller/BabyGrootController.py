#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa


class controller(Sofa.PythonScriptController):
         

    def initGraph(self, node):
            self.node = node
            self.sendDisplacementsToSerial()



    def onEndAnimationStep(self,dt):
        self.sendDisplacementsToSerial()


    def sendDisplacementsToSerial(self):

        cableHeadTop1        = self.node.getChild('babyGroot').getChild('actuator').getObject("cable0").findData('displacement').value #6
        cableHeadTop2        = self.node.getChild('babyGroot').getChild('actuator').getObject("cable1").findData('displacement').value #3

        cableheadLeftBehind  =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable2").findData('displacement').value #12
        cableheadLeftFront   =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable3").findData('displacement').value #10
        cableheadRightBehind =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable4").findData('displacement').value #11
        cableheadRightFront  =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable5").findData('displacement').value #2

        cablehandLeft        =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable6").findData('displacement').value #7
        cablehandLeftBehind  =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable7").findData('displacement').value #13
        cablehandLeftFront   =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable8").findData('displacement').value #9

        cablehandRight       =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable9").findData('displacement').value #4
        # cablehandRightBehind =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable10").findData('displacement').value #1
        cablehandRightFront  =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable11").findData('displacement').value #8

        cablehandHeadRight   =  self.node.getChild('babyGroot').getChild('actuator').getObject("cable12").findData('displacement').value #5


        outputVector = [
        cableheadRightFront + 1.5,
        cableHeadTop2,
        cablehandRight + 38.2,
        cablehandHeadRight + 14.7,
        cableHeadTop1,

        cablehandLeft + 84,
        cablehandRightFront + 45.1,
        cablehandLeftFront + 47.7,
        cableheadLeftFront - 3.5,
        cableheadRightBehind + 4.3,

        cableheadLeftBehind + 6.5,
        cablehandLeftBehind + 58,
        0]


        for i in range(0,13):
            if outputVector[i] < 0:
                outputVector[i] = 0
            outputVector[i] = 255/116*outputVector[i]/1.25
            if outputVector[i] > 250:
                outputVector[i] = 250


        print outputVector
    
        self.node.getObject('serial').findData('sentData').value = outputVector





                



        
