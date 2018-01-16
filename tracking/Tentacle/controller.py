#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import client
import OEFilter
import numpy



def norm(x):
    norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
    return norm


def normalize(x):
    norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
    for i in range(0,3):
        x[i] = x[i]/norm

def LeapToSofa(v):

    temp = v[0]
    v[0] = v[1]
    v[1] = temp

    return v


class controller(Sofa.PythonScriptController):
         

    def initGraph(self, node):

            ### Client initialization
            self.node = node
            self.clientREQ = client.client()

            self.origin = [80, 0, 25]

            
            ### Filter initialization
            filterConfig = {
                'freq': 150,       # Hz
                'mincutoff': 0.1,  # FIXME
                'beta': 0.1,       # FIXME
                'dcutoff': 1.0     # this one should be ok
                }
            
            self.filterVector = []
            for i in range (0,9):
                self.filterVector.append(OEFilter.OneEuroFilter(**filterConfig))

            
    def onBeginAnimationStep(self, dt):

            ### Get the reply.
            self.clientREQ.socket.send(b'Request!')
            vectors = self.clientREQ.socket.recv_pyobj()

            if not isinstance(vectors, int):

                proxDirection = vectors[0] #Proximal joint
                distDirection = vectors[1] #Distal joint
                tipDirection = vectors[2]  #Tip
                normalize(proxDirection)
                normalize(distDirection)
                normalize(tipDirection)
                positions = self.node.getChild('goal').getObject('goalMO').findData('position').value

                ### Frame projection: Leap->Sofa 
                LeapToSofa(proxDirection)
                LeapToSofa(distDirection)
                LeapToSofa(tipDirection)


                ### Apply displacement to index proximal joint position
                proxPosition = numpy.ndarray(3, numpy.double)
                for j in range(0,3):
                    proxPosition[j] = self.origin[j] + proxDirection[j]*70

                ### Goal = filteredLeapPosition
                positions[0][0] = self.filterVector[0](proxPosition[0])
                positions[0][1] = self.filterVector[1](proxPosition[1])
                positions[0][2] = self.filterVector[2](proxPosition[2])


                ### Apply displacement to index distal joint position
                distPosition = numpy.ndarray(3, numpy.double)
                for j in range(0,3):
                    distPosition[j] = proxPosition[j] + distDirection[j]*50

                ### Goal = filteredLeapPosition
                positions[1][0] = self.filterVector[3](distPosition[0])
                positions[1][1] = self.filterVector[4](distPosition[1])
                positions[1][2] = self.filterVector[5](distPosition[2])


                ### Apply displacement to index tip position
                tipPosition = numpy.ndarray(3, numpy.double)
                for j in range(0,3):
                    tipPosition[j] = distPosition[j] + tipDirection[j]*20

                ### Goal = filteredLeapPosition
                positions[2][0] = self.filterVector[6](tipPosition[0])
                positions[2][1] = self.filterVector[7](tipPosition[1])
                positions[2][2] = self.filterVector[8](tipPosition[2])


                self.node.getChild('goal').getObject('goalMO').findData('position').value = positions




                



        
