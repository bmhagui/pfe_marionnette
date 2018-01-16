import zmq
import sys

class client:
  
  def __init__(self):
  	self.context = zmq.Context()
	self.socket = self.context.socket(zmq.REQ)
	self.socket.connect("tcp://localhost:5556")
	print "Connecting to server..."
