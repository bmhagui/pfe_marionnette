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


while True:
    message = socket.recv() # RECEIVE REQUEST
    
    frame = controller.frame()
    hands = frame.hands

    if not hands.is_empty :

        hand = hands[0]

        # hand_x_basis = hand.basis.x_basis
        # hand_y_basis = hand.basis.y_basis
        # hand_z_basis = hand.basis.z_basis
        # hand_origin = hand.finger(1).joint_position(0) # index MCP joint
        # handTransform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
        # handTransform = handTransform.rigid_inverse()

        fingers = hand.fingers

        indexTipDirection = None
        indexDistDirection = None
        indexProxDirection = None


        if not fingers.is_empty:

            for finger in fingers:

                # INDEX
                if finger.type == 1:
                    # TIP
                    indexTipDirection = finger.tip_position
                    indexTipDirection -= finger.joint_position(2)
                    # handTransform.transform_direction(indexTipDirection)

                    # DISTAL
                    indexDistDirection = finger.joint_position(2)
                    indexDistDirection -= finger.joint_position(1)
                    # handTransform.transform_direction(indexDistDirection)

                    # PROXIMAL
                    indexMCPJoint = finger.joint_position(0)
                    indexProxDirection = finger.joint_position(1)
                    indexProxDirection -= indexMCPJoint
                    # handTransform.transform_direction(indexProxDirection)


            # Send only if all is set
            if indexTipDirection is not None and \
            indexDistDirection is not None and \
            indexProxDirection is not None:

                output = numpy.array([[0.,0.,0.]])

                output[0] = indexProxDirection.to_float_array()                    
                output = numpy.append(output,[indexDistDirection.to_float_array()],0)
                output = numpy.append(output,[indexTipDirection.to_float_array()],0)

                socket.send_pyobj(output)

            else:
                socket.send_pyobj(0)
                break
        else:
            socket.send_pyobj(0)
            break
    else:
        socket.send_pyobj(0)

