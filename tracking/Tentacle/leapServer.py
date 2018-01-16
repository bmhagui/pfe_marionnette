import zmq
from random import randrange

import Leap
import server
import numpy
import time

server_instance = server.server()
controller = Leap.Controller()

while True:
    frame = controller.frame()
    hands = frame.hands
    
    for hand in hands:

        fingers = hand.fingers
        palmPosition = hand.palm_position

        thumbTipPosition = None
        indexTipPosition = None
        middleTipPosition = None
        ringTipPosition = None
        pinkyTipPosition = None

        indexPosition = None
        middlePosition = None
        ringPosition = None
        pinkyPosition = None

        for finger in fingers:
            
            # THUMB
            if finger.type == 0:
                thumbTipPosition = finger.tip_position
                thumbTipPosition -= palmPosition
                thumbTipPosition /= finger.length

        # INDEX / TIP
            if finger.type == 1:
                indexTipPosition = finger.tip_position
                indexTipPosition -= palmPosition
                indexTipPosition /= finger.length

            # MIDDLE / TIP
            if finger.type == 2:
                middleTipPosition = finger.tip_position
                middleTipPosition -= palmPosition
                middleTipPosition /= finger.length

        # RING / TIP
            if finger.type == 3:
                ringTipPosition = finger.tip_position
                ringTipPosition -= palmPosition
                ringTipPosition /= finger.length

            # PINKY / TIP
            if finger.type == 4:
                pinkyTipPosition = finger.tip_position
                pinkyTipPosition -= palmPosition
                pinkyTipPosition /= finger.length

        # INDEX / MIDDLE
            if finger.type == 1:
                indexPosition = finger.bone(2).prev_joint
                indexPosition -= palmPosition
                indexPosition /= finger.length

            # MIDDLE / MIDDLE
            if finger.type == 2:
                middlePosition = finger.bone(2).prev_joint
                middlePosition -= palmPosition
                middlePosition /= finger.length

        # RING / MIDDLE
            if finger.type == 3:
                ringPosition = finger.bone(2).prev_joint
                ringPosition -= palmPosition
                ringPosition /= finger.length

            # PINKY / MIDDLE
            if finger.type == 4:
                pinkyPosition = finger.bone(2).prev_joint
                pinkyPosition -= palmPosition
                pinkyPosition /= finger.length


            # Send only if the three are set
            if middleTipPosition is not None and \
            middlePosition is not None and \
            indexTipPosition is not None and \
            indexPosition is not None and \
            ringTipPosition is not None and \
            ringPosition is not None and \
            pinkyTipPosition is not None and \
            pinkyPosition is not None and \
            thumbTipPosition is not None :

                output = numpy.array([[0.,0.,0.]])

                output[0] = middleTipPosition.to_float_array()
                # print middleTipPosition
                # print middleTipPosition.to_float_array()

                time.sleep(0.01)
                server_instance.sendDirection(str(middleTipPosition.x))
                print middleTipPosition.x
                # output = numpy.append(output,[middlePosition.to_float_array()],0)

                # output = numpy.append(output,[indexTipPosition.to_float_array()],0)
                # output = numpy.append(output,[indexPosition.to_float_array()],0)

                # output = numpy.append(output,[pinkyTipPosition.to_float_array()],0)
                # output = numpy.append(output,[pinkyPosition.to_float_array()],0)

                # output = numpy.append(output,[ringTipPosition.to_float_array()],0)
                # output = numpy.append(output,[ringPosition.to_float_array()],0)

                # output = numpy.append(output,[thumbTipPosition.to_float_array()],0)

                
                
