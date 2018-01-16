#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import clientREQ

import numpy


def norm(x):
    norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
    return norm

def normalize(x):
    norm = numpy.sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])
    for i in range(0,3):
        x[i] = x[i]/norm



class controller(Sofa.PythonScriptController):
         

    def initGraph(self, node):

            self.node = node
            self.client = clientREQ.clientREQ()
            self.palmPosition = numpy.array([7.5, -15, -40], numpy.double)


            
    def onBeginAnimationStep(self, dt):

            #Get the reply.
            # vectors = self.client.socket.recv_pyobj()
            self.client.socket.send(b'Hello, World!')
            vectors = self.client.socket.recv_pyobj()

            if not isinstance(vectors, int):
                positionsStr = ""

                for i in range(0,9):

                    vector = vectors[i]
                    position = numpy.ndarray(3, numpy.double)

                    for j in range(0,3):
                        position[j] = vector[j]

                    positionsStr += str(-position[1]) + " " + str(-position[0]) + " " + str(-position[2]) + " "

                self.node.getChild('goal').getObject('goalMO').findData('position').value = positionsStr



        
