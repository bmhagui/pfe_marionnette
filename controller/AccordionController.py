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

        displacement1 = self.node.getChild('accordion').getChild('cables').getObject("cable1").findData('displacement').value 
        displacement2 = self.node.getChild('accordion').getChild('cables').getObject("cable2").findData('displacement').value 
        displacement3 = self.node.getChild('accordion').getChild('cables').getObject("cable3").findData('displacement').value 
        pressure      = self.node.getChild('accordion').getChild('cavity').getObject("pressure").findData('pressure').value 

        output = [displacement3,
        displacement2,
        displacement1,
        pressure*15]

        for i in range(0,3):
            output[i] = (output[i]+0.9)/0.014

        self.node.getObject('serial').findData('sentData').value = output





                



        
