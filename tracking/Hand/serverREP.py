import zmq
import time
import sys
import Leap
import numpy

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

controller = Leap.Controller()

print "serverREQ initialized"


while True:
    message = socket.recv() # RECEIVE REQUEST

    frame = controller.frame()
    hands = frame.hands

    if not hands.is_empty :

        hand = hands[0]

        hand_x_basis = hand.basis.x_basis
        hand_y_basis = hand.basis.y_basis
        hand_z_basis = hand.basis.z_basis
        hand_origin  = hand.palm_position
        handTransform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
        handTransform = handTransform.rigid_inverse()

        fingers = hand.fingers
        palmPosition = hand.palm_position

        thumbTipDirection = None
        indexTipDirection = None
        middleTipDirection = None
        ringTipDirection = None
        pinkyTipDirection = None

        indexDirection = None
        middleDirection = None
        ringDirection = None
        pinkyDirection = None

        if not fingers.is_empty:
            
            for finger in fingers:

                # THUMB
                if finger.type == 0:
                    thumbTipDirection = finger.tip_position
                    thumbTipDirection -= palmPosition
                    handTransform.transform_direction(thumbTipDirection)

                # INDEX / TIP
                if finger.type == 1:
                    indexTipDirection = finger.tip_position
                    indexTipDirection -= palmPosition
                    handTransform.transform_direction(indexTipDirection)

                # MIDDLE / TIP
                if finger.type == 2:
                    middleTipDirection = finger.tip_position
                    middleTipDirection -= palmPosition
                    handTransform.transform_direction(middleTipDirection)

                # RING / TIP
                if finger.type == 3:
                    ringTipDirection = finger.tip_position
                    ringTipDirection -= palmPosition
                    handTransform.transform_direction(ringTipDirection)

                # PINKY / TIP
                if finger.type == 4:
                    pinkyTipDirection = finger.tip_position
                    pinkyTipDirection -= palmPosition
                    handTransform.transform_direction(pinkyTipDirection)

                # INDEX / MIDDLE
                if finger.type == 1:
                    indexDirection = finger.bone(2).prev_joint
                    indexDirection -= palmPosition
                    handTransform.transform_direction(indexDirection)

                # MIDDLE / MIDDLE
                if finger.type == 2:
                    middleDirection = finger.bone(2).prev_joint
                    middleDirection -= palmPosition
                    handTransform.transform_direction(middleDirection)

                # RING / MIDDLE
                if finger.type == 3:
                    ringDirection = finger.bone(2).prev_joint
                    ringDirection -= palmPosition
                    handTransform.transform_direction(ringDirection)

                # PINKY / MIDDLE
                if finger.type == 4:
                    pinkyDirection = finger.bone(2).prev_joint
                    pinkyDirection -= palmPosition
                    handTransform.transform_direction(pinkyDirection)


            # Send only if the three are set
            if middleTipDirection is not None and \
            middleDirection is not None and \
            indexTipDirection is not None and \
            indexDirection is not None and \
            ringTipDirection is not None and \
            ringDirection is not None and \
            pinkyTipDirection is not None and \
            pinkyDirection is not None and \
            thumbTipDirection is not None :

                output = numpy.array([[0.,0.,0.]])

                output[0] = middleTipDirection.to_float_array()                    
                output = numpy.append(output,[middleDirection.to_float_array()],0)

                output = numpy.append(output,[indexTipDirection.to_float_array()],0)
                output = numpy.append(output,[indexDirection.to_float_array()],0)

                output = numpy.append(output,[pinkyTipDirection.to_float_array()],0)
                output = numpy.append(output,[pinkyDirection.to_float_array()],0)

                output = numpy.append(output,[ringTipDirection.to_float_array()],0)
                output = numpy.append(output,[ringDirection.to_float_array()],0)

                output = numpy.append(output,[thumbTipDirection.to_float_array()],0)

                socket.send_pyobj(output)

            else:
                socket.send_pyobj(0)
                break
        else:
            socket.send_pyobj(0)
            break
    else:
        socket.send_pyobj(0)

