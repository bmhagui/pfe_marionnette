import zmq
import time
import sys
import Leap
import numpy

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

controller = Leap.Controller()

print "server initialized"

def dot(v1,v2):
    x = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
    return x

while True:
    message = socket.recv() # RECEIVE REQUEST

    frame = controller.frame()
    hands = frame.hands

    if not hands.is_empty :

        hand = hands[0]

        fingers = hand.fingers
        palmPosition = hand.palm_position

        thumbBasis  = fingers[0].bone(0).basis
        indexBasis  = fingers[1].bone(0).basis
        middleBasis = fingers[2].bone(0).basis
        ringBasis   = fingers[3].bone(0).basis
        pinkyBasis  = fingers[4].bone(0).basis

        fingerBasis = [thumbBasis, indexBasis, middleBasis, ringBasis, pinkyBasis]
        directions = [None]*10
        projections = [None]*10

        if not fingers.is_empty:

            for finger in fingers:

                directions[finger.type*2] = finger.tip_position
                directions[finger.type*2] -= finger.bone(0).prev_joint
                projections[finger.type*2] = [dot(fingerBasis[finger.type].z_basis,directions[finger.type*2]), dot(fingerBasis[finger.type].y_basis,directions[finger.type*2])]

                directions[finger.type*2+1] = finger.bone(2).prev_joint
                directions[finger.type*2+1] -= finger.bone(0).prev_joint
                projections[finger.type*2+1] = [dot(fingerBasis[finger.type].z_basis,directions[finger.type*2+1]), dot(fingerBasis[finger.type].y_basis,directions[finger.type*2+1])]

            # Send only if all is set
            if projections[0] is not None and \
            projections[1] is not None and \
            projections[2] is not None and \
            projections[3] is not None and \
            projections[4] is not None and \
            projections[5] is not None and \
            projections[6] is not None and \
            projections[7] is not None and \
            projections[8] is not None and \
            projections[9] is not None:

                output = [[0.,0.]]*10

                # output[0] = projections[0].to_float_array()
                for i in range(0,10):
                    output[i] = projections[i]

                socket.send_pyobj(output)

            else:
                socket.send_pyobj(0)
                break
        else:
            socket.send_pyobj(0)
            break
    else:
        socket.send_pyobj(0)
