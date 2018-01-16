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

        displacement = self.node.getChild('tentacle').getChild('actuator').getObject("cable").findData('displacement').value 
        print displacement
        displacement = 255/85*(25-displacement)
        if displacement < 0:
            displacement = 0;
        if displacement > 250:
            displacement = 250
    
        self.node.getObject('serial').findData('sentData').value = [displacement]





                



        
