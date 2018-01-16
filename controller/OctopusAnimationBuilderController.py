#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa

def rotate(v,q):

    c0 = ((1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2]))*v[0] + (2.0 * (q[0] * q[1] - q[2] * q[3])) * v[1] + (2.0 * (q[2] * q[0] + q[1] * q[3])) * v[2])
    c1 = ((2.0 * (q[0] * q[1] + q[2] * q[3]))*v[0] + (1.0 - 2.0 * (q[2] * q[2] + q[0] * q[0]))*v[1] + (2.0 * (q[1] * q[2] - q[0] * q[3]))*v[2])
    c2 = ((2.0 * (q[2] * q[0] - q[1] * q[3]))*v[0] + (2.0 * (q[1] * q[2] + q[0] * q[3]))*v[1] + (1.0 - 2.0 * (q[1] * q[1] + q[0] * q[0]))*v[2])

    v[0] = c0
    v[1] = c1
    v[2] = c2

    return v

class controller(Sofa.PythonScriptController):
         

    def initGraph(self, node):
            print "initGraph"
            self.node = node
            self.sendDisplacementsToSerial()
            

    def bwdInitGraph(self, node):
            self.handleMassDistribution()

            
    def onEndAnimationStep(self, dt):
            self.sendDisplacementsToSerial()


    def handleMassDistribution(self):
        #Total mass = 0.350
        #Tentacle mass = 0.014
        #Tentacles mass = 0.070
        #Head mass = 0.280
        #Arbitrary eyes mass = 0.040

        #Nb nodes in head = 190
        #Nb nodes in eyes = 55
        #Nb nodes in tentacles = 570

        #Head mass per node = 0.240/(190-55) = 0.0017
        #Eyes mass per node = 0.040/55 = 0.0009
        #Tentacles mass per node = 0.070/570 = 0.00012

        octopusNode = self.node.getChild('octopus')
        indicesHead = octopusNode.getObject('ROI').findData("indices").value
        indicesEyes = octopusNode.getObject('BoxROI').findData("indices").value
        mass = octopusNode.getObject('DiagMass').findData("mass").value

        for i in range(0,760):

            inHead = False;
            inEyes = False;
            for k in range(0,190):
                if indicesHead[k][0] == i:
                    inHead = True

            for k in range(0,55):
                if indicesEyes[k][0] == i:
                    inHead = False
                    inEyes = True

            if inHead :
                mass[i] = 0.0018
            elif inEyes:
                mass[i] = 0.0007
            else:
                mass[i] = 0.00012

        octopusNode.getObject('DiagMass').findData("mass").value = mass


    def sendDisplacementsToSerial(self):

        cableHead         = 0#self.node.getChild('octopus').getChild('actuator').getObject("cable1").findData('displacement').value

        cableTentacleOut1 = self.node.getChild('octopus').getChild('actuator').getObject("cable2").findData('displacement').value
        cableTentacleOut2 = self.node.getChild('octopus').getChild('actuator').getObject("cable3").findData('displacement').value
        cableTentacleOut3 = self.node.getChild('octopus').getChild('actuator').getObject("cable4").findData('displacement').value
        cableTentacleOut4 = self.node.getChild('octopus').getChild('actuator').getObject("cable5").findData('displacement').value
        cableTentacleOut5 = self.node.getChild('octopus').getChild('actuator').getObject("cable6").findData('displacement').value

        cableEyeR         = self.node.getChild('octopus').getChild('actuator').getObject("cable7").findData('displacement').value
        cableEyeL         = self.node.getChild('octopus').getChild('actuator').getObject("cable8").findData('displacement').value

        cableTentacleIn1 = self.node.getChild('octopus').getChild('actuatorTentacle0').getObject("cable10").findData('displacement').value
        cableTentacleIn2 = self.node.getChild('octopus').getChild('actuatorTentacle1').getObject("cable11").findData('displacement').value
        cableTentacleIn3 = self.node.getChild('octopus').getChild('actuatorTentacle2').getObject("cable12").findData('displacement').value
        cableTentacleIn4 = self.node.getChild('octopus').getChild('actuatorTentacle3').getObject("cable13").findData('displacement').value
        cableTentacleIn5 = self.node.getChild('octopus').getChild('actuatorTentacle4').getObject("cable14").findData('displacement').value

        outputVector = [cableHead , #+ 12.153, 
                        cableTentacleIn1 + 1.7 ,
                        cableTentacleIn5 + 0.4 ,
                        cableTentacleIn3 - 2 ,
                        cableTentacleIn4 + -2 ,
                        cableTentacleIn2 + 0.4 , 
                        cableEyeR + 9, cableEyeL + 9,
                        cableTentacleOut1 + 30.7, 
                        cableTentacleOut2 + 23.3,
                        cableTentacleOut3 + 8,
                        cableTentacleOut4 + 8,
                        cableTentacleOut5 + 23.3,
                        ]


        # for disp in outputVector: 
        #     if disp<self.minDisp:
        #         self.minDisp = disp
        #     if disp>self.maxDisp:
        #         self.maxDisp = disp

        # print self.minDisp
        # print self.maxDisp

        minDisp = 19
        for i in range(0,13):
            if outputVector[i] < 0:
                outputVector[i] = 0
            outputVector[i] = 255/115*outputVector[i]

        # print outputVector            
        #Cable entre -19 et 115
    
        self.node.getObject('serial').findData('sentData').value = outputVector



                



        
