#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa

import os, sys, inspect
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import client
import OEFilter
import numpy


def norm(x):
    norm = 0
    if x.size == 3:
        norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
    if x.size == 2:
        norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1])
    return norm


def normalize(x,size):
    if size == 3:
        norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
        for i in range(0,3):
            x[i] = x[i]/norm

    if size == 2:
        norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1])
        for i in range(0,2):
            x[i] = x[i]/norm


def addRotationToList(list, v1, v2, reverseDirection):
    ### Scalar product to get the rotation angle
    v = (v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2])/(norm(v1)*norm(v2))
    teta = numpy.arccos(v)

    if reverseDirection:
        teta = 3.14159*2. - teta

    ### Quaternion: rotation of teta around z axis
    q = [0., .0, numpy.sin(teta/2.), numpy.cos(teta/2.)]
    list.append(q)

    return list


def rotate(v,q):

    c0 = ((1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2]))*v[0] + (2.0 * (q[0] * q[1] - q[2] * q[3])) * v[1] + (2.0 * (q[2] * q[0] + q[1] * q[3])) * v[2])
    c1 = ((2.0 * (q[0] * q[1] + q[2] * q[3]))*v[0] + (1.0 - 2.0 * (q[2] * q[2] + q[0] * q[0]))*v[1] + (2.0 * (q[1] * q[2] - q[0] * q[3]))*v[2])
    c2 = ((2.0 * (q[2] * q[0] - q[1] * q[3]))*v[0] + (2.0 * (q[1] * q[2] + q[0] * q[3]))*v[1] + (1.0 - 2.0 * (q[1] * q[1] + q[0] * q[0]))*v[2])

    v[0] = c0
    v[1] = c1
    v[2] = c2

    return v


def inverseRotate(v,q):

    c0 = ((1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2]))*v[0] + (2.0 * (q[0] * q[1] + q[2] * q[3])) * v[1] + (2.0 * (q[2] * q[0] - q[1] * q[3])) * v[2])
    c1 = ((2.0 * (q[0] * q[1] - q[2] * q[3]))*v[0] + (1.0 - 2.0 * (q[2] * q[2] + q[0] * q[0]))*v[1] + (2.0 * (q[1] * q[2] + q[0] * q[3]))*v[2])
    c2 = ((2.0 * (q[2] * q[0] + q[1] * q[3]))*v[0] + (2.0 * (q[1] * q[2] - q[0] * q[3]))*v[1] + (1.0 - 2.0 * (q[1] * q[1] + q[0] * q[0]))*v[2])

    v[0] = c0
    v[1] = c1
    v[2] = c2

    return v



class controller(Sofa.PythonScriptController):



    def initGraph(self, node):

            ### Client initialization
            self.node = node
            self.clientREQ = client.client()

            self.sendDisplacementsToSerial()

            ### Mapping initialization
            self.tentacleDirections    = []
            self.initialSofaNorms      = numpy.ndarray(10, numpy.double)

            self.headPosition = numpy.array([0, 0, 30], numpy.double)
            for i in range(0,5):
                positions     = node.getChild('filteredGoal').getObject('goalMO').findData('position').value
                
                self.tentacleDirections.append(positions[i*2+1] - self.headPosition)
                copy = numpy.array([positions[i*2+1][0], positions[i*2+1][1], positions[i*2+1][2]], numpy.double)
                self.tentacleDirections.append(positions[i*2+2] - copy)

                self.initialSofaNorms[i*2] = norm(self.tentacleDirections[i*2])
                self.initialSofaNorms[i*2+1] = norm(self.tentacleDirections[i*2+1])
                self.tentacleDirections[i*2][2] = 0.
                normalize(self.tentacleDirections[i*2], 3)


            ### Filter initialization
            filterConfig = {
                'freq': 150,       # Hz
                'mincutoff': 0.1,  # FIXME
                'beta': 0.1,       # FIXME
                'dcutoff': 1.0     # this one should be ok
                }

            self.filterVector = []
            for i in range (0,30):
                self.filterVector.append(OEFilter.OneEuroFilter(**filterConfig))



    def LeapToSofa(self, v, i):

        x = v[0]
        y = v[1]

        v=[0,0,0]
        v[0]=-x*self.tentacleDirections[i*2][0]
        v[1]=-x*self.tentacleDirections[i*2][1]
        v[2]=y

        normalize(v,3)

        v[0]*=self.initialSofaNorms[i*2] 
        v[1]*=self.initialSofaNorms[i*2] 
        v[2]*=self.initialSofaNorms[i*2] 

        return v


    def bwdInitGraph(self, node):
            self.handleMassDistribution()


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


    def onBeginAnimationStep(self, dt):

            ### Get the reply.
            self.clientREQ.socket.send('Request!')
            vectors = self.clientREQ.socket.recv_pyobj()


            if not isinstance(vectors, int):


                ### Loop on fingers tip and middle position
                for i in range(0,5):

                    #Vector in 2D (on tentacle/finger plan)
                    vector1 = vectors[i*2]
                    vector1 = self.LeapToSofa(vector1, i) #Projection in Sofa 3D scene

                    vector2 = vectors[i*2+1]
                    vector2 = self.LeapToSofa(vector2, i) #Projection in Sofa 3D scene

                    ### Normalize to Sofa dimension
                    v1   = [vector1[0],vector1[1],vector1[2]]
                    v2   = [vector2[0],vector2[1],vector2[2]]
 	 	    #print (vector1[2])
		    print (vector2[2])

                    ### Apply displacement to goal position
                    position1 = numpy.ndarray(3, numpy.double)
                    for j in range(0,3):
                        position1[j] = self.headPosition[j] + v2[j]

                    position2 = numpy.ndarray(3, numpy.double)
                    for j in range(0,3):
                        position2[j] = self.headPosition[j] + v1[j]


                    ### Goal = filteredLeapPosition
                    positions = self.node.getChild('filteredGoal').getObject('goalMO').findData('position').value

                    filteredPosition1 = self.filterVector[(i*3)*2](position1[0])
                    filteredPosition2 = self.filterVector[(i*3+1)*2](position1[1])
                    filteredPosition3 = self.filterVector[(i*3+2)*2](position1[2])

                    positions[i*2+1][0] = filteredPosition1
                    positions[i*2+1][1] = filteredPosition2
                    positions[i*2+1][2] = filteredPosition3

                    filteredPosition1 = self.filterVector[(i*3)*2+1](position2[0])
                    filteredPosition2 = self.filterVector[(i*3+1)*2+1](position2[1])
                    filteredPosition3 = self.filterVector[(i*3+2)*2+1](position2[2])

                    positions[i*2+2][0] = filteredPosition1
                    positions[i*2+2][1] = filteredPosition2
                    positions[i*2+2][2] = filteredPosition3

                    self.node.getChild('filteredGoal').getObject('goalMO').findData('position').value = positions



    def onEndAnimationStep(self, dt):
        self.sendDisplacementsToSerial()



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
        cableTentacleIn2 = self.node.getChild('octopus').getChild('actuatorTentacle4').getObject("cable14").findData('displacement').value
        cableTentacleIn3 = self.node.getChild('octopus').getChild('actuatorTentacle2').getObject("cable12").findData('displacement').value
        cableTentacleIn4 = self.node.getChild('octopus').getChild('actuatorTentacle3').getObject("cable13").findData('displacement').value
        cableTentacleIn5 = self.node.getChild('octopus').getChild('actuatorTentacle1').getObject("cable11").findData('displacement').value

        outputVector = [cableTentacleIn1 + 1.7 ,
                        cableTentacleIn2 + 0.4 ,
                        cableTentacleIn3 - 2 ,
                        cableTentacleIn4 + -2 ,
                        cableTentacleIn5 + 0.4 ,
                        cableEyeR + 9,
                        cableEyeL + 9,
                        cableTentacleOut1 + 30.7,
                        cableTentacleOut2 + 23.3,
                        cableTentacleOut3 + 8,
                        cableTentacleOut4 + 8,
                        cableTentacleOut5 + 23.3,
                        ]


        for i in range(0,12):
            if outputVector[i] < 0:
                outputVector[i] = 0
            outputVector[i] = 255/116*outputVector[i]
            if outputVector[i] > 250:
                outputVector[i] = 250

        print outputVector
        #Cable entre -19 et 115

        self.node.getObject('serial').findData('sentData').value = outputVector
