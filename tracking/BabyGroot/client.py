import zmq
import sys

class client:
  
  def __init__(self):
    
    self.port = "5556"
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.SUB)
    print "Connecting to server..."
    self.socket.connect("tcp://localhost:%s" % self.port)
    self.socket.setsockopt(zmq.SUBSCRIBE,'')
    


