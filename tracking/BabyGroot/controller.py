import Sofa
import client


#Communication avec Sofa 
class controller(Sofa.PythonScriptController):
  
	def onLoaded(self,node):
		print 'Controller script loaded from node %s'%node.findData('name').value
		return 0


	def initGraph(self,node):
	  
		self.client = client.client()
		self.goalState = node.getObject('goalMO')
		
		# Get the reply.
		ratio_x = self.client.socket.recv()	
		self.goalState.findData('position').value = str(-100 + float(ratio_x)*200) + ' -41.28 248.407   23.521 -28.055 150.95';
		
		return 0


	def onBeginAnimationStep(self,dt):

		# Get the reply.
		ratio_x = self.client.socket.recv()	
		self.goalState.findData('position').value = str(-100 + float(ratio_x)*200) + ' -41.28 248.407   23.521 -28.055 150.95';

		return 0
