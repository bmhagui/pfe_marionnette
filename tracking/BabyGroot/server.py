import zmq
import time
import sys


class server :

  def __init__(self):
    
    self.port = "5556"
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PUB)
  
    self.socket.bind("tcp://*:%s" % self.port)
    print ("Server initializated")


  def sendPosition(self,ratio_x):
    
    return self.socket.send(ratio_x) 
